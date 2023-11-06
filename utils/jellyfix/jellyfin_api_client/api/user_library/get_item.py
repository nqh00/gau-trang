from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.base_item_dto import BaseItemDto
from ...types import Response


def _get_kwargs(
    user_id: str,
    item_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/Users/{userId}/Items/{itemId}".format(
            userId=user_id,
            itemId=item_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BaseItemDto]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = BaseItemDto.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, BaseItemDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, BaseItemDto]]:
    """Gets an item from a user's library.

    Args:
        user_id (str):
        item_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseItemDto]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        item_id=item_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, BaseItemDto]]:
    """Gets an item from a user's library.

    Args:
        user_id (str):
        item_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseItemDto]
    """

    return sync_detailed(
        user_id=user_id,
        item_id=item_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, BaseItemDto]]:
    """Gets an item from a user's library.

    Args:
        user_id (str):
        item_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseItemDto]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        item_id=item_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, BaseItemDto]]:
    """Gets an item from a user's library.

    Args:
        user_id (str):
        item_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseItemDto]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            item_id=item_id,
            client=client,
        )
    ).parsed
