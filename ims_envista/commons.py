"""IMS Envista Commons."""

import http
import logging
import uuid
from json import JSONDecodeError
from typing import Any

from aiohttp import (
    ClientError,
    ClientSession,
    TraceRequestChunkSentParams,
    TraceRequestEndParams,
    TraceRequestStartParams,
)

logger = logging.getLogger(__name__)

class IMSEnvistaError(Exception):
    """
    Exception raised for errors in the IMS Envista API.

    Attributes
    ----------
        error -- description of the error

    """

    def __init__(self, error: str) -> None:
        self.error = error
        super().__init__(f"{self.error}")

async def on_request_start_debug(session: ClientSession, context,params: TraceRequestStartParams) -> None:  # noqa: ANN001, ARG001
    logger.debug("HTTP %s: %s", params.method, params.url)


async def on_request_chunk_sent_debug(
    session: ClientSession, context, params: TraceRequestChunkSentParams  # noqa: ANN001, ARG001
) -> None:
    if (params.method in ("POST", "PUT")) and params.chunk:
        logger.debug("HTTP Content %s: %s", params.method, params.chunk)


async def on_request_end_debug(session: ClientSession, context, params: TraceRequestEndParams) -> None:  # noqa: ANN001, ARG001
    response_text = await params.response.text()
    logger.debug("HTTP %s Response <%s>: %s", params.method, params.response.status, response_text)


def get_headers(token: uuid | str) -> dict[str, str]:
    return {
        "Accept": "application/vnd.github.v3.text-match+json",
        "Authorization": f"ApiToken {token!s}"
    }

async def get(
    session: ClientSession, url: str, token: str | uuid, headers: dict | None = None
) -> dict[str, Any]:
    try:
        if not headers:
            headers = get_headers(token)

        resp = await session.get(url=url, headers=headers)
        json_resp: dict = await resp.json(content_type=None)
    except TimeoutError as ex:
        msg = f"Failed to communicate with IMS Envista API due to time out: ({ex!s})"
        raise IMSEnvistaError(msg) from ex
    except ClientError as ex:
        msg = f"Failed to communicate with  IMS Envistadue to ClientError: ({ex!s})"
        raise IMSEnvistaError(msg) from ex
    except JSONDecodeError as ex:
        msg = f"Received invalid response from IMS Envista API: {ex!s}"
        raise IMSEnvistaError(msg) from ex

    if resp.status != http.HTTPStatus.OK:
        msg = f"Received Error from IMS Envista API: {resp.status, resp.reason}"
        raise IMSEnvistaError(msg)

    return json_resp
