import pytest
import requests
from unittest.mock import patch, MagicMock

from main import inspect_request, build_parser


def test_inspect_request_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = "https://httpbin.org/anything"
    mock_response.json.return_value = {"key": "value"}

    with patch("requests.request", return_value=mock_response) as mock_req:
        result = inspect_request(
            "GET",
            "https://httpbin.org/anything"
        )

        assert result["status_code"] == 200
        assert result["method"] == "GET"
        assert result["body"] == {"key": "value"}
        assert "response_time_ms" in result

        mock_req.assert_called_once_with(
            method="GET",
            url="https://httpbin.org/anything",
            params=None,
            headers=None,
            json=None,
            timeout=10,
        )


def test_inspect_request_non_json():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = "https://httpbin.org/anything"
    mock_response.json.side_effect = ValueError("No JSON")
    mock_response.text = "Plain text response"

    with patch("requests.request", return_value=mock_response):
        result = inspect_request(
            "GET",
            "https://httpbin.org/anything"
        )

        assert result["body"] == "Plain text response"


def test_inspect_request_timeout():
    with patch("requests.request", side_effect=requests.Timeout):
        with pytest.raises(requests.Timeout):
            inspect_request(
                "GET",
                "https://httpbin.org/anything"
            )


def test_argument_parser():
    parser = build_parser()

    args = parser.parse_args([
        "--method", "POST",
        "--json", '{"a": 1}',
        "--timeout", "5.5"
    ])

    assert args.method == "POST"
    assert args.json_body == '{"a": 1}'
    assert args.timeout == 5.5
