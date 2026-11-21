
"""Unit tests for the HTTP request inspection toolkit."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from main import build_parser, inspect_request


HTTPBIN_URL = "https://httpbin.org/anything"


def test_inspect_request_success():
    """Test successful HTTP request inspection."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = HTTPBIN_URL
    mock_response.json.return_value = {"key": "value"}

    with patch(
        "main.requests.request",
        return_value=mock_response,
    ) as mock_request:
        result = inspect_request("GET", HTTPBIN_URL)

    assert result["status_code"] == 200
    assert result["method"] == "GET"
    assert result["url"] == HTTPBIN_URL
    assert result["body"] == {"key": "value"}
    assert "response_time_ms" in result
    assert result["response_time_ms"] >= 0

    mock_request.assert_called_once_with(
        method="GET",
        url=HTTPBIN_URL,
        params=None,
        headers=None,
        json=None,
        timeout=10,
    )


def test_inspect_request_non_json():
    """Test handling of responses that are not valid JSON."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = HTTPBIN_URL
    mock_response.json.side_effect = ValueError("No JSON")
    mock_response.text = "Plain text response"

    with patch(
        "main.requests.request",
        return_value=mock_response,
    ):
        result = inspect_request("GET", HTTPBIN_URL)

    assert result["status_code"] == 200
    assert result["body"] == "Plain text response"


def test_inspect_request_timeout():
    """Test that request timeouts are propagated correctly."""
    with patch(
        "main.requests.request",
        side_effect=requests.Timeout,
    ):
        with pytest.raises(requests.Timeout):
            inspect_request("GET", HTTPBIN_URL)


def test_argument_parser():
    """Test parsing of command-line arguments."""
    parser = build_parser()

    args = parser.parse_args(
        [
            "--method",
            "POST",
            "--json",
            '{"a": 1}',
            "--timeout",
            "5.5",
        ]
    )

    assert args.method == "POST"
    assert args.json_body == '{"a": 1}'
    assert args.timeout == 5.5
