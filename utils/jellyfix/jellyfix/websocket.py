import asyncio
import logging
from typing import Any, Optional

import aiohttp
from typing_extensions import NotRequired, TypedDict


class JellyfinWebSocketClient:
    """
    A client to the jellyfin websocket.

    For a basic usage, you can use :method:`jellyfix.JellyfinClient.listen`
    directly.
    Subclass me for more advanced stuff!
    """

    def __init__(self, logger: Optional[logging.Logger]):
        if not logger:
            logger = logging.getLogger(__name__)
        self._log = logger

        self.__keep_alive_task: Optional[asyncio.Task] = None

    async def listen(self, base_url: str, token: str, device_id: str):
        """
        Establish the connection and wait for events.

        Keep alive events are automatically handled.

        :param base_url: Base URL of the Jellyfin server, eg
            https://jellyfin.example.org
        :param token: The authorization token
        :param device_id: String to identify this device
        """
        self._log.debug("Connecting to %s", base_url)
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(
                f"ws{base_url.removeprefix('http')}/socket",
                params={"api_key": token, "device_id": device_id},
            ) as ws:
                self._log.info("Connected to %s", base_url)
                async for msg in ws:
                    self._log.debug("WS-RECV: %s", msg)
                    # the following line is just a workaround for pycharm
                    # mis-detecting the type of msg (mypy gets it right, though)
                    msg: aiohttp.WSMessage  # type:ignore
                    if msg.type == aiohttp.WSMsgType.ERROR:
                        self._log.error("Websocket received: %s, closing", msg)
                        break
                    event = msg.json()
                    await self.__handle_event(ws, event)

    async def send(
        self,
        ws: aiohttp.ClientWebSocketResponse,
        event_type: str,
        data: Optional[Any] = None,
    ):
        """
        Sand an event to jellyfin via the websocket
        """
        payload = {"MessageType": event_type, "Data": data}
        self._log.debug("WS-SEND: %s", payload)
        await ws.send_json(payload)

    async def __handle_event(self, ws: aiohttp.ClientWebSocketResponse, event: "Event"):
        if event["MessageType"] == "ForceKeepAlive":
            if self.__keep_alive_task:
                self.__keep_alive_task.cancel()
            self.__keep_alive_task = asyncio.create_task(self.__keep_alive(ws, event["Data"]))
        elif event["MessageType"] == "KeepAlive":
            pass
        else:
            await self.handle_event(event["MessageType"], event.get("Data"))

    async def __keep_alive(self, ws: aiohttp.ClientWebSocketResponse, timeout: int):
        while True:
            await self.send(ws, "KeepAlive")
            await asyncio.sleep(timeout / 2)

    async def handle_event(self, event_type: str, data: Optional[Any]):
        """
        Default event handler, that does nothing but log the incoming events.

        Override me!
        """
        self._log.debug("Received event %s with data %s", event_type, data)


class Event(TypedDict):
    """
    The content of a raw Jellyfin event.

    Maybe later, we'll add proper event types, all annotated.
    """

    MessageType: str
    MessageId: str
    Data: NotRequired[Any]
