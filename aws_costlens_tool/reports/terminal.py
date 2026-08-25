from __future__ import annotations

from decimal import Decimal

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aws_costlens_tool.models.finding import Finding

console = Console()


def _display_width() -> int:
    """Return a balanced display width for CostLens output."""
    return min(max(80, console.size.width - 4), 110)



def show_logo() -> None:
    """Display the AWS CostLens banner."""

    large_logo = r"""
 █████╗ ██╗    ██╗███████╗     ██████╗ ██████╗ ███████╗████████╗██╗     ███████╗███╗   ██╗███████╗
██╔══██╗██║    ██║██╔════╝    ██╔════╝██╔═══██╗██╔════╝╚══██╔══╝██║     ██╔════╝████╗  ██║██╔════╝
███████║██║ █╗ ██║███████╗    ██║     ██║   ██║███████╗   ██║   ██║     █████╗  ██╔██╗ ██║███████╗
██╔══██║██║███╗██║╚════██║    ██║     ██║   ██║╚════██║   ██║   ██║     ██╔══╝  ██║╚██╗██║╚════██║
██║  ██║╚███╔███╔╝███████║    ╚██████╗╚██████╔╝███████║   ██║   ███████╗███████╗██║ ╚████║███████║
╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝     ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝
"""

    compact_logo = r"""
   AWS COSTLENS
"""

    if console.size.width >= 105:
        console.print(f"[bold cyan]{large_logo}[/bold cyan]")
    else:
        console.print(f"[bold cyan]{compact_logo}[/bold cyan]", justify="center")

    console.print(
        "[dim]Lightweight · Read-only AWS FinOps CLI[/dim]",
        justify="center",
    )
    console.print()



def show_header(account: str, region: str, arn: str) -> None:
    console.print(
        Panel.fit(
            f"[bold]🏥 AWS COSTLENS CHECKUP[/bold]\n"
            f"Account : {account}\n"
            f"Region  : {region}\n"
            f"Identity: {arn}",
            border_style="cyan",
        )
    )


def show_cost_summary(summary: dict) -> None:
    table = Table(title="💰 Cost Summary")
    table.add_column("Metric")
    table.add_column("Value", justify="right")

    table.add_row("Current MTD", _money(summary["current_cost"]))
    table.add_row("Previous Month", _money(summary["previous_cost"]))

    change = summary.get("change_pct")
    table.add_row("Change", "N/A" if change is None else f"{change:+.1f}%")
    console.print(table)

    services = Table(title="Top Service Cost Drivers")
    services.add_column("Service")
    services.add_column("Cost", justify="right")
    for item in summary.get("services", []):
        services.add_row(item["service"], _money(item["cost"]))
    console.print(services)


def show_credits(result: dict) -> None:
    if not result.get("available"):
        console.print(
            Panel(
                f"[yellow]Credit check skipped[/yellow]\n"
                f"{result.get('error_code')}: {result.get('message')}",
                title="💳 AWS Credit",
            )
        )
        return

    credits = result.get("credits", [])
    if not credits:
        console.print(Panel("No credits returned for the query period.", title="💳 AWS Credit"))
        return

    table = Table(title="💳 AWS Credit")
    table.add_column("Name")
    table.add_column("Status")
    table.add_column("Initial", justify="right")
    table.add_column("Remaining", justify="right")
    table.add_column("Est. Remaining", justify="right")
    table.add_column("Expiration")

    for credit in credits:
        table.add_row(
            str(credit.get("name") or "AWS Credit"),
            str(credit.get("status") or ""),
            _optional_money(credit.get("initial")),
            _optional_money(credit.get("remaining")),
            _optional_money(credit.get("estimated_remaining")),
            str(credit.get("expiration") or ""),
        )
    console.print(table)


def show_findings(findings: list[Finding]) -> None:
    """Display findings grouped by type."""

    if not findings:
        console.print(
            Panel(
                "No findings detected by the enabled checks.",
                title="🩺 Findings",
                width=_display_width(),
                border_style="green",
            )
        )
        return

    grouped = {}

    for finding in findings:
        key = (
            finding.severity,
            finding.resource_type,
            finding.title,
        )

        if key not in grouped:
            grouped[key] = {
                "count": 0,
                "cost": 0.0,
                "has_cost": False,
            }

        grouped[key]["count"] += 1

        if finding.estimated_monthly_cost_usd is not None:
            grouped[key]["cost"] += finding.estimated_monthly_cost_usd
            grouped[key]["has_cost"] = True

    severity_order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
        "INFO": 4,
    }

    ordered = sorted(
        grouped.items(),
        key=lambda item: (
            severity_order.get(item[0][0].upper(), 99),
            item[0][1],
            item[0][2],
        ),
    )

    table = Table(
        title="🩺 Findings Summary",
        width=_display_width(),
        expand=True,
    )

    table.add_column("Severity", ratio=1)
    table.add_column("Resource", ratio=2)
    table.add_column("Finding", ratio=5)
    table.add_column("Count", justify="right", ratio=1)
    table.add_column("Est. Cost/Mo", justify="right", ratio=2)

    for (severity, resource_type, title), data in ordered:
        if data["has_cost"]:
            cost = f"${data['cost']:.2f}"
        else:
            cost = "Review"

        table.add_row(
            severity,
            resource_type,
            title,
            str(data["count"]),
            cost,
        )

    console.print(table)

    console.print(
        f"[dim]Total findings: {len(findings)} · "
        f"Finding types: {len(grouped)}[/dim]"
    )


def show_recommendations(findings: list[Finding]) -> None:
    """Display unique recommendations."""

    if not findings:
        return

    recommendations = []

    for finding in findings:
        recommendation = finding.recommendation.strip()

        if recommendation and recommendation not in recommendations:
            recommendations.append(recommendation)

    lines = [
        f"{index}. {recommendation}"
        for index, recommendation in enumerate(
            recommendations[:6],
            start=1,
        )
    ]

    if len(recommendations) > 6:
        lines.append(
            f"... and {len(recommendations) - 6} more recommendation(s)"
        )

    estimated = sum(
        finding.estimated_monthly_cost_usd or 0.0
        for finding in findings
    )

    lines.append(
        f"\n[bold]Estimated identified monthly waste:[/bold] "
        f"${estimated:.2f}"
    )

    console.print(
        Panel(
            "\n".join(lines),
            title="💊 Recommendations",
        )
    )


def _money(value: Decimal) -> str:
    return f"${value:.2f}"


def _optional_money(value: object) -> str:
    if value in (None, ""):
        return ""
    try:
        return f"${Decimal(str(value)):.2f}"
    except Exception:
        return str(value)


def show_resource_tags(records: list[dict], errors: list[str] | None = None) -> None:
    """Display tagging status for cost-relevant AWS resources."""

    table = Table(
        title="🏷️ Resource Tagging",
        width=_display_width(),
    )

    table.add_column("Service")
    table.add_column("Resource")
    table.add_column("Status")
    table.add_column("Tags")

    tagged = 0
    untagged = 0

    for item in records:
        status = item.get("status", "UNTAGGED")

        if status == "TAGGED":
            tagged += 1
            status_text = "[green]TAGGED[/green]"
        else:
            untagged += 1
            status_text = "[yellow]UNTAGGED[/yellow]"

        tags = item.get("tags", {})

        if tags:
            tag_items = list(tags.items())

            visible = [
                f"{key}={value}"
                for key, value in tag_items[:3]
            ]

            remaining = len(tag_items) - 3

            if remaining > 0:
                visible.append(f"+{remaining} more")

            tag_text = ", ".join(visible)
        else:
            tag_text = "-"

        table.add_row(
            str(item.get("service", "")),
            str(item.get("resource", "")),
            status_text,
            tag_text,
        )

    if records:
        console.print(table)

        console.print(
            f"[green]Tagged[/green]   : {tagged}\n"
            f"[yellow]Untagged[/yellow] : {untagged}\n"
            f"Total    : {len(records)}"
        )
    else:
        console.print(
            Panel(
                "No supported resources were returned.",
                title="🏷️ Resource Tagging",
            )
        )

    if errors:
        console.print(
            f"[dim]Tag checks skipped for {len(errors)} service(s) "
            f"because of permissions or API errors.[/dim]"
        )


def show_resource_tags(records, errors=None):
    """Display EC2, RDS, and S3 resource tagging status."""

    table = Table(
        title="🏷️ Resource Tagging",
        width=_display_width(),
    )

    table.add_column("Service", style="cyan", ratio=1)
    table.add_column("Resource", ratio=3)
    table.add_column("Status", ratio=1)
    table.add_column("Tags", ratio=5)

    tagged = 0
    untagged = 0

    for item in records:
        status = item["status"]
        tags = item.get("tags", {})

        if status == "TAGGED":
            tagged += 1
            status_text = "[green]TAGGED[/green]"
        else:
            untagged += 1
            status_text = "[yellow]UNTAGGED[/yellow]"

        if tags:
            tag_items = list(tags.items())

            # 최대 3개까지만 표시
            visible = [
                f"{key}={value}"
                for key, value in tag_items[:3]
            ]

            remaining = len(tag_items) - 3

            if remaining > 0:
                visible.append(f"+{remaining} more")

            tag_text = ", ".join(visible)
        else:
            tag_text = "-"

        table.add_row(
            item["service"],
            item["resource"],
            status_text,
            tag_text,
        )

    console.print(table)

    console.print(
        f"[green]Tagged[/green]   : {tagged}    "
        f"[yellow]Untagged[/yellow] : {untagged}    "
        f"Total : {len(records)}"
    )

    if errors:
        console.print(
            f"[dim]Skipped {len(errors)} service(s) due to "
            f"permissions or API errors.[/dim]"
        )
