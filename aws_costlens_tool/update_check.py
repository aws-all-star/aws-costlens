from __future__ import annotations

import json
import shutil
import subprocess
from importlib.metadata import PackageNotFoundError, version

PACKAGE_NAME = "aws-costlens-tool"
FORMULA = "aws-all-star/tap/aws-costlens"


def current_version() -> str:
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        return "unknown"


def latest_version() -> str | None:
    if shutil.which("brew") is None:
        return None

    try:
        # Refresh Homebrew metadata quietly.
        subprocess.run(
            ["brew", "update"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30,
            check=False,
        )

        result = subprocess.run(
            ["brew", "info", "--json=v2", FORMULA],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )

        data = json.loads(result.stdout)

        formulae = data.get("formulae", [])

        if not formulae:
            return None

        stable = formulae[0].get("versions", {}).get("stable")

        return str(stable) if stable else None

    except Exception:
        return None


def _version_tuple(value: str) -> tuple[int, ...]:
    try:
        return tuple(
            int(x)
            for x in value.lstrip("v").split(".")
        )
    except ValueError:
        return (0,)


def update_available() -> tuple[str, str] | None:
    current = current_version()
    latest = latest_version()

    if current == "unknown" or not latest:
        return None

    if _version_tuple(latest) > _version_tuple(current):
        return current, latest

    return None
