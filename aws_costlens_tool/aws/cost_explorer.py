from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

import boto3


def _month_start(value: date) -> date:
    return value.replace(day=1)


def _previous_month_start(value: date) -> date:
    first = _month_start(value)
    return (first - timedelta(days=1)).replace(day=1)


def _amount(result: dict) -> Decimal:
    total = result.get("Total", {}).get("UnblendedCost", {}).get("Amount", "0")
    return Decimal(total)


def get_cost_summary(session: boto3.Session, top_n: int = 8) -> dict:
    ce = session.client("ce", region_name="us-east-1")
    today = date.today()
    current_start = _month_start(today)
    previous_start = _previous_month_start(today)

    current = ce.get_cost_and_usage(
        TimePeriod={"Start": current_start.isoformat(), "End": today.isoformat()},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
    )

    previous = ce.get_cost_and_usage(
        TimePeriod={"Start": previous_start.isoformat(), "End": current_start.isoformat()},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
    )

    by_service = ce.get_cost_and_usage(
        TimePeriod={"Start": current_start.isoformat(), "End": today.isoformat()},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    current_cost = _amount(current["ResultsByTime"][0]) if current.get("ResultsByTime") else Decimal("0")
    previous_cost = _amount(previous["ResultsByTime"][0]) if previous.get("ResultsByTime") else Decimal("0")

    services: list[dict] = []
    if by_service.get("ResultsByTime"):
        for group in by_service["ResultsByTime"][0].get("Groups", []):
            services.append(
                {
                    "service": group["Keys"][0],
                    "cost": Decimal(group["Metrics"]["UnblendedCost"]["Amount"]),
                }
            )

    services.sort(key=lambda item: item["cost"], reverse=True)

    change_pct = None
    if previous_cost != 0:
        change_pct = ((current_cost - previous_cost) / previous_cost) * Decimal("100")

    return {
        "current_cost": current_cost,
        "previous_cost": previous_cost,
        "change_pct": change_pct,
        "services": services[:top_n],
        "currency": "USD",
    }
