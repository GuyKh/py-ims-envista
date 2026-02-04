"""IMS Envista Commons."""

import asyncio
import http
import logging
import socket
from json import JSONDecodeError
from typing import Any
from uuid import UUID

import async_timeout
from aiohttp import ClientError, ClientResponse, ClientSession

_LOGGER = logging.getLogger(__name__)


class ImsEnvistaApiClientError(Exception):
    """Exception to indicate a general API error."""


class ImsEnvistaApiClientCommunicationError(
    ImsEnvistaApiClientError,
):
    """Exception to indicate a communication error."""


class ImsEnvistaApiClientAuthenticationError(
    ImsEnvistaApiClientError,
):
    """Exception to indicate an authentication error."""


def _get_headers(token: UUID | str) -> dict[str, str]:
    return {
        "Accept": "application/vnd.github.v3.text-match+json",
        "Authorization": f"ApiToken {token!s}",
    }


def _verify_response_or_raise(response: ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        _LOGGER.debug("Bad Response: %s", response.text())
        msg = "Invalid credentials"
        raise ImsEnvistaApiClientAuthenticationError(
            msg,
        )
    content_type = response.headers.get("Content-Type")
    if content_type and "application/json" not in content_type:
        _LOGGER.debug("Bad Response: %s", response.text())
        msg = f"Invalid response from IMS - bad Content-Type: {content_type}"
        raise ImsEnvistaApiClientError(
            msg,
        )
    response.raise_for_status()


async def get(
    session: ClientSession, url: str, token: UUID | str, headers: dict | None = None
) -> dict[str, Any]:
    if not headers:
        headers = _get_headers(token)

    try:
        async with async_timeout.timeout(180):
            _LOGGER.debug("Sending GET from %s", url)
            response = await session.get(url=url, headers=headers)
            _verify_response_or_raise(response)
            json_resp = await response.json()

    except (TimeoutError, asyncio.exceptions.TimeoutError) as exception:
        msg = f"Timeout error fetching information from {url} - {exception}"
        raise ImsEnvistaApiClientCommunicationError(
            msg,
        ) from exception
    except (ClientError, socket.gaierror) as exception:
        msg = f"Error fetching information from {url} - {exception}"
        raise ImsEnvistaApiClientCommunicationError(
            msg,
        ) from exception
    except JSONDecodeError as exception:
        msg = f"Failed Parsing Response JSON from {url} - {exception!s}"
        raise ImsEnvistaApiClientError(msg) from exception
    except Exception as exception:  # pylint: disable=broad-except
        msg = f"Something really wrong happened! {url} {exception}"
        raise ImsEnvistaApiClientError(
            msg,
        ) from exception

    _LOGGER.debug("Response from %s: %s", url, json_resp)
    if response.status != http.HTTPStatus.OK:
        msg = f"Received Error from IMS Envista API from {url}: {response.status, response.reason}"
        raise ImsEnvistaApiClientError(msg)

    return json_resp
