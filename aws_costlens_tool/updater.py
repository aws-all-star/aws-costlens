from __future__ import annotations

import shutil
import subprocess

FORMULA = "aws-all-star/tap/aws-costlens"


def run_update() -> None:
    if shutil.which("brew") is None:
        raise RuntimeError(
            "Homebrew was not found."
        )

    print("Refreshing Homebrew...")
    subprocess.run(
        ["brew", "update"],
        check=True,
    )

    print()
    print("Upgrading AWS CostLens...")

    subprocess.run(
        ["brew", "upgrade", FORMULA],
        check=True,
    )
