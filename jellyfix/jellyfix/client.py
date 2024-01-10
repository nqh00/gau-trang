import json
import logging
import os
from pathlib import Path
from socket import gethostname
from typing import Any, AsyncIterator, Awaitable, Callable, Iterator, Literal, Optional, ParamSpec, TypeVar, overload
from uuid import uuid4

import platformdirs

from jellyfin_api_client.api.item_update import update_item
from jellyfin_api_client.api.items import get_items
from jellyfin_api_client.api.user import authenticate_user_by_name
from jellyfin_api_client.api.user_library import get_item
from jellyfin_api_client.client import AuthenticatedClient, Client
from jellyfin_api_client.models import AuthenticateUserByName, BaseItemDto, BaseItemKind
from jellyfin_api_client.types import Response

from .__version__ import VERSION
from .websocket import JellyfinWebSocketClient

P = ParamSpec("P")
T = TypeVar("T")


class JellyfinClient:
    """
    High-level interface to interact with a Jellyfin server.

    When used for the first time as given user, ``base_url`` must be specified
    and the ``login`` method must be called. This will store credentials
    permanently in the user's dedicated dir, usually ``~/.config/jellyfix``
    in linux, and it can then be instantiated without arguments.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        app_name="jellyfix",
        device: Optional[str] = None,
        device_id: Optional[str] = None,
        storage: Optional[os.PathLike] = None,
    ):
        if storage is None:
            storage_path = self.__get_default_storage(app_name)
        else:
            storage_path = Path(storage)

        self._log = logging.getLogger(f"JellyfinClient:{base_url}")
        self.__storage = storage_path

        if device is None:
            device = gethostname()
        if device_id is None:
            device_id = uuid4().hex

        if self.__storage.exists():
            self._log.info("Credentials found at %s", self.__storage)
            self.__load_auth()
            self.logged = True
            self.__set_client()
            return

        self._log.info("Stored credentials not found, login() need to be called.")

        if not base_url:
            raise RuntimeError("You must specify a base URL if you login for the first time")

        self.base_url = base_url
        self.app_name = app_name
        self.device = device
        self.device_id = device_id

        self.user_id: Optional[str] = None
        self.token: Optional[str] = None
        self.client: Optional[AuthenticatedClient] = None
        self.logged = False

    @staticmethod
    def __get_default_storage(app_name: str) -> Path:
        """
        Return the default user storage dir, in a cross-platform-happy way.
        """
        d = platformdirs.user_config_path(app_name)
        d.mkdir(exist_ok=True)
        return d / "credentials.json"

    def __save_auth(self) -> None:
        """
        Writes credentials to disk
        """
        self._log.info("Saving credentials to %s", self.__storage)
        with self.__storage.open("w") as fp:
            json.dump(
                {
                    "user_id": self.user_id,
                    "base_url": self.base_url,
                    "device": self.device,
                    "device_id": self.device_id,
                    "app_name": self.app_name,
                    "token": self.token,
                },
                fp,
            )

    def __load_auth(self) -> None:
        """
        Loads credentials to disk
        """
        self._log.debug("Loading credentials from %s", self.__storage)
        with self.__storage.open("r") as fp:
            saved = json.load(fp)
        for k, v in saved.items():
            setattr(self, k, v)

    def __set_client(self) -> None:
        if not self.token:
            raise RuntimeError("No token?! This should not happen.")
        self.client = AuthenticatedClient(
            self.base_url,
            headers={
                "x-emby-authorization": self.__get_emby_header(),
                "X-MediaBrowser-Token": self.token,
            },
            token="x",  # unused by jellyfin, but required by AuthenticatedClient
            follow_redirects=True,
        )

    def __get_emby_header(self) -> str:
        r = (
            f"MediaBrowser "
            f"Client={self.app_name}, "
            f"Device={self.device}, "
            f"DeviceId={self.device_id}, "
            f"Version={VERSION}"
        )
        if self.user_id:
            r += f", UserId={self.user_id}"
        return r

    def __call(self, method: Callable[..., T], **kwargs: Any) -> T:
        if not self.client:
            raise RuntimeError("Not authenticated!")
        return method(client=self.client, **kwargs)

    @staticmethod
    def __raise_from_resp(resp: Response) -> None:
        if not (200 <= resp.status_code < 400):
            raise RuntimeError(resp)

    def __get_items(
        self,
        page_size: int,
        types: Optional[list[BaseItemKind]] = None,
        search_term: Optional[str] = None,
        **kwargs,
    ) -> Iterator[BaseItemDto]:
        i = 0
        while True:
            resp = self.__call(
                get_items.sync_detailed,
                user_id=self.user_id,
                limit=page_size,
                include_item_types=types,
                search_term=search_term,
                recursive=True,
                start_index=i,
                **kwargs,
            )
            self.__raise_from_resp(resp)
            parsed = resp.parsed
            assert parsed
            assert isinstance(parsed.items, list)
            if not parsed.items:
                break
            for item in parsed.items:
                yield item
            i = (parsed.start_index or 0) + page_size

    async def __get_items_async(
        self,
        page_size: int,
        types: Optional[list[BaseItemKind]] = None,
        search_term: Optional[str] = None,
        **kwargs,
    ) -> AsyncIterator[BaseItemDto]:
        i = 0
        while True:
            resp = await self.__call(
                get_items.asyncio_detailed,
                user_id=self.user_id,
                limit=page_size,
                include_item_types=types,
                recursive=True,
                start_index=i,
                search_term=search_term,
                **kwargs,
            )
            self.__raise_from_resp(resp)
            parsed = resp.parsed
            assert parsed
            assert isinstance(parsed.items, list)
            if not parsed.items:
                break
            for item in parsed.items:
                yield item
            i = (parsed.start_index or 0) + page_size

    def login(self, username: str, password: Optional[str] = None) -> None:
        """
        Calls the AuthenticateUserByName endpoint to get a token.

        The token will then be stored on disk.
        """
        client = Client(
            self.base_url,
            headers={"x-emby-authorization": self.__get_emby_header()},
            follow_redirects=True,
        )
        with client as client:
            resp = authenticate_user_by_name.sync_detailed(
                client=client,
                json_body=AuthenticateUserByName(username=username, pw=password),
            )
        if not (200 <= resp.status_code < 400):
            raise RuntimeError(resp)

        assert resp.parsed
        assert resp.parsed.user
        assert resp.parsed.user.id
        assert resp.parsed.access_token
        self.user_id = resp.parsed.user.id
        self.token = resp.parsed.access_token

        self.__set_client()
        self.logged = True
        self.__save_auth()

    @overload
    def get_item(self, item_id: str) -> BaseItemDto:
        ...

    @overload
    def get_item(self, item_id: str, sync: Literal[True]) -> BaseItemDto:
        ...

    @overload
    def get_item(self, item_id: str, sync: Literal[False]) -> Awaitable[BaseItemDto]:
        ...

    def get_item(self, item_id: str, sync=True):
        """
        Get an item by its id.

        :param item_id: The ID of the item to retrieve.
        :param sync: Set to False for an async call, changing the return type
            to an awaitable.
        """
        if not self.client or not self.user_id:
            raise RuntimeError("Not logged")
        if sync:
            func = get_item.sync
        else:
            func = get_item.asyncio
        return func(client=self.client, user_id=self.user_id, item_id=item_id)

    @overload
    def update_item(self, item: BaseItemDto) -> BaseItemDto:
        ...

    @overload
    def update_item(self, item: BaseItemDto, sync: Literal[True]) -> BaseItemDto:
        ...

    @overload
    def update_item(self, item: BaseItemDto, sync: Literal[False]) -> Awaitable[BaseItemDto]:
        ...

    def update_item(self, item: BaseItemDto, sync=True):
        """
        Updates an item.

        :param item: The object to modify. Make sure to fill in all the fields,
            unset fields will be erased.
        :param sync: Set to False for an async call, changing the return type
            to an awaitable.
        """
        if not self.client:
            raise RuntimeError("Not logged")
        assert item.id
        if sync:
            func = update_item.sync
        else:
            func = update_item.asyncio
        return func(client=self.client, item_id=item.id, json_body=item)

    @overload
    def get_movies(self) -> Iterator[BaseItemDto]:
        ...

    @overload
    def get_movies(self, *, sync: Literal[True]) -> Iterator[BaseItemDto]:
        ...

    @overload
    def get_movies(self, *, sync: Literal[False]) -> AsyncIterator[BaseItemDto]:
        ...

    def get_movies(self, page_size=100, sync=True):
        """
        Iterates over all movies.

        :param page_size: How many items should be fetched at once.
        :param sync: Set to False for an async call, changing the return type
            to an async iterator.
        """
        if sync:
            return self.__get_items(types=[BaseItemKind.MOVIE], page_size=page_size)
        else:
            return self.__get_items_async(types=[BaseItemKind.MOVIE], page_size=page_size)

    @overload
    def get_series(self) -> Iterator[BaseItemDto]:
        ...

    @overload
    def get_series(self, sync: Literal[True]) -> Iterator[BaseItemDto]:
        ...

    @overload
    def get_series(self, sync: Literal[False]) -> AsyncIterator[BaseItemDto]:
        ...

    def get_series(self, page_size=100, sync=True):
        """
        Iterates over all TV shows.

        :param page_size: How many items should be fetched at once.
        :param sync: Set to False for an async call, changing the return type
            to an async iterator.
        """
        if sync:
            return self.__get_items(types=[BaseItemKind.SERIES], page_size=page_size)
        else:
            return self.__get_items_async(types=[BaseItemKind.SERIES], page_size=page_size)

    @overload
    def search_items(self, search_term: str) -> Iterator[BaseItemDto]:
        ...

    @overload
    def search_items(self, search_term: str, *, sync: Literal[True]) -> Iterator[BaseItemDto]:
        ...

    @overload
    def search_items(self, search_term: str, *, sync: Literal[False]) -> AsyncIterator[BaseItemDto]:
        ...

    def search_items(self, search_term: str, *, page_size=100, sync=True):
        """
        Search items in the library/

        :param search_term: Free input for search terms.
        :param page_size: How many items should be fetched at once.
        :param sync: Set to False for an async call, changing the return type
            to an async iterator.
        """
        if sync:
            return self.__get_items(search_term=search_term, page_size=page_size)
        else:
            return self.__get_items_async(search_term=search_term, page_size=page_size)

    async def listen(self, event_handler: Optional[Callable[[str, Any], Awaitable[None]]] = None):
        """
        Connects to the websocket and wait for incoming events.

        :param event_handler: A coroutine taking two parameters: event_type and
            event_data.
        """
        ws = JellyfinWebSocketClient(self._log)
        if event_handler:
            ws.handle_event = event_handler  # type:ignore
        if not self.token:
            raise RuntimeError("You need to login first")
        await ws.listen(self.base_url, self.token, self.device_id)
