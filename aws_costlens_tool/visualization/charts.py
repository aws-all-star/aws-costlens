from __future__ import annotations

from datetime import datetime

from rich.console import Console

console = Console()


def _bar(value: float, maximum: float, width: int = 22) -> str:
    if maximum <= 0 or value <= 0:
        return ""

    size = max(1, round((value / maximum) * width))
    return "█" * size


def show_terminal_cost_charts(
    cost_summary: dict,
    daily_costs: list[dict],
    daily_limit: int = 7,
) -> None:
    services = cost_summary.get("services", [])

    console.print()
    console.print("[bold cyan]AWS Cost by Service[/bold cyan]")
    console.print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    console.print()

    if services:
        rows = []

        for item in services:
            try:
                cost = float(item.get("cost", 0))
            except (TypeError, ValueError):
                cost = 0.0

            rows.append(
                {
                    "service": str(item.get("service", "Unknown")),
                    "cost": cost,
                }
            )

        rows.sort(key=lambda x: x["cost"], reverse=True)

        total = sum(item["cost"] for item in rows)
        maximum = max((item["cost"] for item in rows), default=0)

        for item in rows:
            name = item["service"]
            cost = item["cost"]
            percent = (cost / total * 100) if total else 0

            console.print(
                f"{name[:22]:22} "
                f"${cost:9.2f}  "
                f"[cyan]{_bar(cost, maximum)}[/cyan] "
                f"{percent:5.1f}%"
            )

    else:
        console.print("[dim]No service cost data available.[/dim]")

    console.print()
    console.print(
        f"[bold cyan]Daily Cost Trend (Last {daily_limit} Days)[/bold cyan]"
    )
    console.print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    console.print()

    recent = daily_costs[-daily_limit:]

    if recent:
        values = []

        for item in recent:
            try:
                cost = float(item.get("cost", 0))
            except (TypeError, ValueError):
                cost = 0.0

            values.append(
                (
                    str(item.get("date", "")),
                    cost,
                )
            )

        maximum = max((cost for _, cost in values), default=0)

        for raw_date, cost in values:
            try:
                label = datetime.strptime(
                    raw_date,
                    "%Y-%m-%d",
                ).strftime("%b %d")
            except ValueError:
                label = raw_date

            console.print(
                f"{label:8} "
                f"${cost:8.2f}  "
                f"[cyan]{_bar(cost, maximum)}[/cyan]"
            )

    else:
        console.print("[dim]No daily cost data available.[/dim]")

    console.print()
