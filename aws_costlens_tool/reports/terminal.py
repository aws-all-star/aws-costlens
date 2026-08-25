from __future__ import annotations

from decimal import Decimal

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aws_costlens_tool.models.finding import Finding

console = Console()


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
    table = Table(title="🩺 Findings")
    table.add_column("Severity")
    table.add_column("Resource")
    table.add_column("Finding")
    table.add_column("Est. Cost/Mo", justify="right")

    for finding in findings:
        cost = (
            f"${finding.estimated_monthly_cost_usd:.2f}"
            if finding.estimated_monthly_cost_usd is not None
            else "Review"
        )
        table.add_row(
            finding.severity,
            finding.resource_type,
            finding.title,
            cost,
        )

    if findings:
        console.print(table)
    else:
        console.print(Panel("No findings detected by the enabled checks.", title="🩺 Findings"))


def show_recommendations(findings: list[Finding]) -> None:
    if not findings:
        return

    lines = []
    for index, finding in enumerate(findings, start=1):
        lines.append(f"{index}. [{finding.severity}] {finding.recommendation}")

    estimated = sum(
        finding.estimated_monthly_cost_usd or 0.0
        for finding in findings
    )
    lines.append(f"\nEstimated identified monthly waste: ${estimated:.2f}")
    console.print(Panel("\n".join(lines), title="💊 Recommendations"))


def _money(value: Decimal) -> str:
    return f"${value:.2f}"


def _optional_money(value: object) -> str:
    if value in (None, ""):
        return ""
    try:
        return f"${Decimal(str(value)):.2f}"
    except Exception:
        return str(value)
