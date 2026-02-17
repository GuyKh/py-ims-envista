"""Unit tests for HTTP helpers."""

from __future__ import annotations

from ims_envista.commons import _get_headers


def test_get_headers_uses_json_accept_and_api_token() -> None:
    headers = _get_headers("abc123")

    assert headers["Accept"] == "application/json"
    assert headers["Authorization"] == "ApiToken abc123"
