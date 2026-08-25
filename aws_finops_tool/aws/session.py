from __future__ import annotations

import boto3


def get_session(profile: str | None = None, region: str | None = None) -> boto3.Session:
    kwargs: dict[str, str] = {}
    if profile:
        kwargs["profile_name"] = profile
    if region:
        kwargs["region_name"] = region
    return boto3.Session(**kwargs)


def get_identity(session: boto3.Session) -> dict[str, str]:
    sts = session.client("sts")
    identity = sts.get_caller_identity()
    return {
        "account": identity["Account"],
        "arn": identity["Arn"],
    }
