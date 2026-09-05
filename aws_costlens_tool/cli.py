from __future__ import annotations

import typer
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound

from aws_costlens_tool.aws.billing import get_credits
from aws_costlens_tool.aws.cost_explorer import get_cost_summary, get_daily_costs
from aws_costlens_tool.aws.session import get_identity, get_session
from aws_costlens_tool.checks.ebs import check_unattached_ebs
from aws_costlens_tool.checks.eip import check_unassociated_eips
from aws_costlens_tool.checks.stopped_ec2 import check_stopped_instances
from aws_costlens_tool.checks.tags import scan_resource_tags
from aws_costlens_tool.config import DEFAULT_REGION
from aws_costlens_tool.update_check import update_available
from aws_costlens_tool.visualization.charts import show_terminal_cost_charts
from aws_costlens_tool.reports.terminal import (
    console,
    show_cost_summary,
    show_credits,
    show_findings,
    show_header,
    show_logo,
    show_recommendations,
    show_resource_tags,
)

app = typer.Typer(help="Read-only AWS FinOps cost and waste checkup CLI")

@app.callback()
def main() -> None:
    """AWS CostLens CLI."""
    show_logo()

    try:
        update = update_available()

        if update:
            current, latest = update

            console.print(
                f"[yellow]⬆ New AWS CostLens version available: "
                f"v{current} → v{latest}[/yellow]"
            )
            console.print(
                "[bold]Run:[/bold] aws-costlens update"
            )
            console.print()

    except Exception:
        # Update checks must never interrupt normal commands.
        pass


def _session(profile: str | None, region: str):
    try:
        return get_session(profile=profile, region=region)
    except ProfileNotFound as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=2) from exc


@app.command()
def check(
    profile: str | None = typer.Option(None, help="AWS CLI profile name"),
    region: str = typer.Option(DEFAULT_REGION, help="AWS workload region"),
) -> None:
    """Run cost, credit, and resource waste checks."""
    session = _session(profile, region)

    try:
        identity = get_identity(session)
        show_header(identity["account"], region, identity["arn"])

        try:
            show_cost_summary(get_cost_summary(session))
        except (ClientError, BotoCoreError) as exc:
            console.print(f"[yellow]Cost Explorer check skipped:[/yellow] {exc}")

        show_credits(get_credits(session, identity["account"]))

        findings = []
        for runner in (
            check_unassociated_eips,
            check_unattached_ebs,
            check_stopped_instances,
        ):
            try:
                findings.extend(runner(session, region))
            except (ClientError, BotoCoreError) as exc:
                console.print(f"[yellow]{runner.__name__} skipped:[/yellow] {exc}")

        tag_records, tag_errors = scan_resource_tags(session, region)

        show_findings(findings)
        show_resource_tags(tag_records, tag_errors)
        show_recommendations(findings)

    except (ClientError, BotoCoreError) as exc:
        console.print(f"[red]AWS API error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def cost(
    profile: str | None = typer.Option(None, help="AWS CLI profile name"),
    region: str = typer.Option(DEFAULT_REGION, help="AWS workload region"),
    days: int = typer.Option(7, min=1, max=90, help="Daily cost trend period"),
) -> None:
    """Show AWS cost summary and terminal visualization."""
    session = _session(profile, region)
    identity = get_identity(session)

    show_header(identity["account"], region, identity["arn"])

    try:
        summary = get_cost_summary(session)
        daily = get_daily_costs(session, days=days)

        show_cost_summary(summary)
        show_terminal_cost_charts(summary, daily, daily_limit=days)

    except (ClientError, BotoCoreError) as exc:
        console.print(f"[red]AWS API error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def credit(
    profile: str | None = typer.Option(None, help="AWS CLI profile name"),
    region: str = typer.Option(DEFAULT_REGION, help="AWS workload region"),
) -> None:
    """Show AWS promotional credit information when permitted."""
    session = _session(profile, region)
    identity = get_identity(session)
    show_header(identity["account"], region, identity["arn"])
    
    try:
        show_credits(get_credits(session, identity["account"]))
    except (ClientError, BotoCoreError, TypeError, ValueError) as exc:
        console.print(
            f"[yellow]Credit check skipped:[/yellow] {exc}"
    )

@app.command()
def waste(
    profile: str | None = typer.Option(None, help="AWS CLI profile name"),
    region: str = typer.Option(DEFAULT_REGION, help="AWS workload region"),
) -> None:
    """Run resource waste checks only."""
    session = _session(profile, region)
    identity = get_identity(session)
    show_header(identity["account"], region, identity["arn"])

    findings = []
    findings.extend(check_unassociated_eips(session, region))
    findings.extend(check_unattached_ebs(session, region))
    findings.extend(check_stopped_instances(session, region))

    tag_records, tag_errors = scan_resource_tags(session, region)

    show_findings(findings)
    show_resource_tags(tag_records, tag_errors)
    show_recommendations(findings)

@app.command()
def update() -> None:
    """Update AWS CostLens to the latest Homebrew release."""
    from aws_costlens_tool.update_check import current_version, latest_version
    from aws_costlens_tool.updater import run_update

    console.print()
    console.print("[bold cyan]AWS CostLens Update[/bold cyan]")
    console.print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    console.print()

    current = current_version()
    latest = latest_version(timeout=5.0)

    console.print(f"Current version: [bold]v{current}[/bold]")

    if not latest:
        console.print("[red]Unable to check the latest release.[/red]")
        raise typer.Exit(code=1)

    console.print(f"Latest version:  [bold]v{latest}[/bold]")
    console.print()

    if current == latest:
        console.print(
            "[green]✓ AWS CostLens is already up to date.[/green]"
        )
        return

    console.print(
        f"[yellow]Updating v{current} → v{latest}...[/yellow]"
    )
    console.print()

    try:
        run_update()
    except Exception as exc:
        console.print()
        console.print(f"[red]Update failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print()
    console.print(
        f"[green]✓ AWS CostLens v{latest} update completed.[/green]"
    )

if __name__ == "__main__":
    app()
