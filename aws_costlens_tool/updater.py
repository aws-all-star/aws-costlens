from __future__ import annotations

import shutil
import subprocess

from aws_costlens_tool.update_check import current_version, latest_version

FORMULA = "aws-all-star/tap/aws-costlens"


def run_update() -> tuple[str, str]:
    current = current_version()
    latest = latest_version(timeout=5.0)

    if not latest:
        raise RuntimeError(
            "Unable to determine the latest AWS CostLens version."
        )

    if current == latest:
        return current, latest

    if shutil.which("brew") is None:
        raise RuntimeError(
            "Homebrew was not found. "
            "Update AWS CostLens using the original installation method."
        )

    subprocess.run(
        ["brew", "update"],
        check=True,
    )

    subprocess.run(
        ["brew", "upgrade", FORMULA],
        check=True,
    )

    return current, latest
