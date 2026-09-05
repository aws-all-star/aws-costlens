from __future__ import annotations

import json
import urllib.request
from importlib.metadata import PackageNotFoundError, version

PACKAGE_NAME = "aws-costlens-tool"
LATEST_URL = "https://api.github.com/repos/aws-all-star/aws-costlens/releases/latest"


def current_version() -> str:
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        return "0.0.0"


def _version_tuple(value: str) -> tuple[int, ...]:
    value = value.lstrip("v")
    result = []

    for part in value.split("."):
        try:
            result.append(int(part))
        except ValueError:
            break

    return tuple(result)


def latest_version(timeout: float = 1.5) -> str | None:
    try:
        request = urllib.request.Request(
            LATEST_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "aws-costlens",
            },
        )

        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.load(response)

        latest = str(payload.get("tag_name", "")).lstrip("v")
        return latest or None

    except Exception:
        # Update checking must NEVER break normal CLI execution.
        return None


def update_available() -> tuple[str, str] | None:
    current = current_version()
    latest = latest_version()

    if not latest:
        return None

    if _version_tuple(latest) > _version_tuple(current):
        return current, latest

    return None
