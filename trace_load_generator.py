"""Generate recurring traced requests for the Week 6 tracing activity."""

import argparse
import json
import random
import time
import urllib.error
import urllib.request
from typing import Optional


def build_request(url: str, method: str = "GET", data: Optional[dict] = None,
                 token: Optional[str] = None) -> urllib.request.Request:
    """Build an HTTP request with optional JSON body and bearer token."""
    headers = {"Content-Type": "application/json"}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    body = None if data is None else json.dumps(data).encode("utf-8")
    return urllib.request.Request(url, data=body, headers=headers, method=method)


def request_json(request: urllib.request.Request) -> tuple[int, Optional[dict]]:
    """Execute a request and return its status code and parsed JSON body."""
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode("utf-8")
            payload = json.loads(raw) if raw else None
            return response.status, payload
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        payload = json.loads(raw) if raw else None
        return error.code, payload


def register_user(base_url: str) -> str:
    """Register a unique demo user and return the issued token."""
    username = f"trace-user-{random.randint(100000, 999999)}"
    payload = {"username": username, "name": "Trace Demo", "password": "password123"}
    request = build_request(f"{base_url}/auth/register", method="POST", data=payload)
    status, body = request_json(request)
    if status not in (200, 201) or not body or "token" not in body:
        raise RuntimeError(f"registration failed with status {status}")
    return body["token"]


def main() -> None:
    """Run the recurring traced request loop."""
    parser = argparse.ArgumentParser(description="Generate traced todo requests.")
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()

    token = register_user(args.base_url)
    print("Registered demo user; token retained (not printed).")

    invalid_id = "not-a-valid-object-id"
    try:
        while True:
            status, _ = request_json(build_request(f"{args.base_url}/todos/", token=token))
            print(f"GET /todos/ -> {status}")

            status, body = request_json(build_request(
                f"{args.base_url}/todos/", method="POST", data={"title": "trace todo"}, token=token))
            print(f"POST /todos/ -> {status}")
            created_id = body.get("id") if isinstance(body, dict) else None

            if created_id:
                status, _ = request_json(build_request(f"{args.base_url}/todos/{created_id}", token=token))
                print(f"GET /todos/{created_id} -> {status}")

            status, _ = request_json(build_request(f"{args.base_url}/todos/{invalid_id}", token=token))
            print(f"GET /todos/{invalid_id} -> {status}")

            time.sleep(random.uniform(0.1, args.delay + 0.5))
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
