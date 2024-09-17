import http
import logging
import uuid
from json import JSONDecodeError
from typing import Any, Optional

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

    def __init__(self, error) -> None:
        self.error = error
        super().__init__(f"{self.error}")

async def on_request_start_debug(session: ClientSession, context, params: TraceRequestStartParams):
    logger.debug(f"HTTP {params.method}: {params.url}")


async def on_request_chunk_sent_debug(
    session: ClientSession, context, params: TraceRequestChunkSentParams
):
    if (params.method == "POST" or params.method == "PUT") and params.chunk:
        logger.debug(f"HTTP Content {params.method}: {params.chunk}")


async def on_request_end_debug(session: ClientSession, context, params: TraceRequestEndParams):
    logger.debug(f"HTTP {params.method} Response <{params.response.status}>: {await params.response.text()}")


def get_headers(token: uuid | str):
    return {
        "Accept": "application/vnd.github.v3.text-match+json",
        "Authorization": f"ApiToken {str(token)}"
    }

async def get(
    session: ClientSession, url: str, token: str | uuid,  timeout: Optional[int] = 60, headers: Optional[dict] = None
) -> dict[str, Any]:
    try:
        if not headers:
            headers = get_headers(token)

        resp = await session.get(url=url, headers=headers, timeout=timeout)
        json_resp: dict = await resp.json(content_type=None)
    except TimeoutError as ex:
        raise IMSEnvistaError(f"Failed to communicate with IMS Envista API due to time out: ({str(ex)})")
    except ClientError as ex:
        raise IMSEnvistaError(f"Failed to communicate with  IMS Envistadue to ClientError: ({str(ex)})")
    except JSONDecodeError as ex:
        raise IMSEnvistaError(f"Received invalid response from IMS Envista API: {str(ex)}")

    if resp.status != http.HTTPStatus.OK:
        raise IMSEnvistaError(f"Received Error from IMS Envista API: {resp.status, resp.reason}")

    return json_resp
