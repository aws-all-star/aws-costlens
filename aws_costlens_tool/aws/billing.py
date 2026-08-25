from __future__ import annotations

import time
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError


def get_credits(session: boto3.Session, account_id: str) -> dict:
    client = session.client("billing", region_name="us-east-1")
    one_year_ago = int(time.time()) - (365 * 24 * 60 * 60)

    try:
        response = client.get_credits(
            accountId=account_id,
            startDate=one_year_ago,
        )
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "Unknown")
        message = exc.response.get("Error", {}).get("Message", str(exc))
        return {
            "available": False,
            "error_code": code,
            "message": message,
            "credits": [],
        }

    credits = []
    for credit in response.get("credits", []):
        credits.append(
            {
                "name": credit.get("name") or credit.get("description") or "AWS Credit",
                "status": credit.get("creditStatus"),
                "initial": credit.get("initialAmount", {}).get("currencyAmount"),
                "remaining": credit.get("remainingAmount", {}).get("currencyAmount"),
                "estimated_remaining": credit.get("estimatedAmount", {}).get("currencyAmount"),
                "currency": credit.get("remainingAmount", {}).get("currencyCode", "USD"),
                "expiration": _format_epoch(credit.get("endDate")),
            }
        )

    return {"available": True, "credits": credits}


def _format_epoch(value: int | float | datetime | None) -> str | None:
    if value is None:
        return None

    if isinstance(value, datetime):
        return value.date().isoformat()

    return datetime.fromtimestamp(
        value,
        tz=timezone.utc,
    ).date().isoformat()
