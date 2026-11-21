"""A small CLI tool for inspecting HTTP requests with httpbin.org."""

import argparse
import json
import sys
import time
from typing import Any

import requests


DEFAULT_URL = "https://httpbin.org/anything"


def inspect_request( method: str, url: str, *, params: dict[str, Any] | None = None, headers: dict[str, str] | None = None, json_body: Any | None = None, timeout: float = 10, ) -> dict[str, Any]:
    """Send an HTTP request and return a concise inspection result."""
    started = time.perf_counter()

    response = requests.request(
        method=method.upper(),
        url=url,
        params=params,
        headers=headers,
        json=json_body,
        timeout=timeout,
    )

    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    response.raise_for_status()

    try:
        body: Any = response.json()
    except ValueError:
        body = response.text

    return {
        "status_code": response.status_code,
        "method": method.upper(),
        "url": response.url,
        "response_time_ms": elapsed_ms,
        "body": body,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Send an HTTP request and inspect the response."
    )
    parser.add_argument(
        "--method",
        default="GET",
        choices=["GET", "POST", "PUT", "PATCH", "DELETE"],
        help="HTTP method (default: GET)",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Request URL (default: {DEFAULT_URL})",
    )
    parser.add_argument(
        "--json",
        dest="json_body",
        help="JSON request body, supplied as a JSON string",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10,
        help="Request timeout in seconds (default: 10)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        payload = json.loads(args.json_body) if args.json_body else None
        result = inspect_request(
            args.method,
            args.url,
            json_body=payload,
            timeout=args.timeout,
        )
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 2
    except requests.Timeout:
        print("Request timed out.", file=sys.stderr)
        return 1
    except requests.ConnectionError:
        print("Could not connect to the server.", file=sys.stderr)
        return 1
    except requests.HTTPError as exc:
        print(f"HTTP error: {exc}", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
