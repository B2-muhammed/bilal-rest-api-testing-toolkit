import requests
from unittest.mock import Mock, patch

import pytest

from main import inspect_request


@patch("main.requests.request")
def test_get_request_inspection(mock_request):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.url = "https://httpbin.org/anything"
    mock_response.json.return_value = {
        "method": "GET",
        "url": "https://httpbin.org/anything",
    }

    mock_request.return_value = mock_response

    result = inspect_request(
        method="GET",
        url="https://httpbin.org/anything",
    )

    assert result["status_code"] == 200
    assert result["method"] == "GET"
    assert result["body"]["method"] == "GET"
    assert result["elapsed_ms"] >= 0

    mock_request.assert_called_once()


@patch("main.requests.request")
def test_post_json_payload(mock_request):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.url = "https://httpbin.org/anything"
    mock_response.json.return_value = {
        "json": {"name": "Bilal", "project": "REST API Toolkit"}
    }

    mock_request.return_value = mock_response

    payload = {
        "name": "Bilal",
        "project": "REST API Toolkit",
    }

    result = inspect_request(
        method="POST",
        url="https://httpbin.org/anything",
        json_body=payload,
    )

    assert result["status_code"] == 200
    assert result["body"]["json"] == payload

    mock_request.assert_called_once_with(
        method="POST",
        url="https://httpbin.org/anything",
        params=None,
        headers=None,
        json=payload,
        timeout=10,
    )


@patch("main.requests.request")
def test_http_error_handling(mock_request):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError("404 Not Found")
    )

    mock_request.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        inspect_request(
            method="GET",
            url="https://httpbin.org/status/404",
        )
