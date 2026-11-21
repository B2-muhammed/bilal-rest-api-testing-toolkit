import argparse
import time

import requests


def inspect_request(
    method,
    url,
    params=None,
    headers=None,
    json_body=None,
    timeout=10,
):
    start_time = time.perf_counter()

    response = requests.request(
        method=method.upper(),
        url=url,
        params=params,
        headers=headers,
        json=json_body,
        timeout=timeout,
    )

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    response.raise_for_status()

    try:
        body = response.json()
    except ValueError:
        body = response.text

    return {
        "status_code": response.status_code,
        "method": method.upper(),
        "url": response.url,
        "elapsed_ms": round(elapsed_ms, 2),
        "body": body,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Python HTTP request inspection toolkit"
    )

    parser.add_argument(
        "--method",
        default="GET",
        choices=["GET", "POST", "PUT", "PATCH", "DELETE"],
    )
    parser.add_argument(
        "--url",
        default="https://httpbin.org/anything",
    )
    parser.add_argument("--json", dest="json_body")
    parser.add_argument("--timeout", type=float, default=10)

    args = parser.parse_args()

    try:
        import json

        payload = json.loads(args.json_body) if args.json_body else None

        result = inspect_request(
            method=args.method,
            url=args.url,
            json_body=payload,
            timeout=args.timeout,
        )

        print(json.dumps(result, indent=4))

    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")
    except requests.exceptions.RequestException as error:
        print(f"Request error: {error}")
    except ValueError as error:
        print(f"Invalid JSON: {error}")


if __name__ == "__main__":
    main()
