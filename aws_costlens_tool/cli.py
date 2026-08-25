from __future__ import annotations

import typer
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound

from aws_costlens.aws.billing import get_credits
from aws_costlens.aws.cost_explorer import get_cost_summary
from aws_costlens.aws.session import get_identity, get_session
from aws_costlens.checks.ebs import check_unattached_ebs
from aws_costlens.checks.eip import check_unassociated_eips
from aws_costlens.checks.stopped_ec2 import check_stopped_instances
from aws_costlens.config import DEFAULT_REGION
from aws_costlens.reports.terminal import (
    console,
    show_cost_summary,
    show_credits,
    show_findings,
    show_header,
    show_recommendations,
)

app = typer.Typer(help="Read-only AWS FinOps cost and waste checkup CLI")


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

        show_findings(findings)
        show_recommendations(findings)

    except (ClientError, BotoCoreError) as exc:
        console.print(f"[red]AWS API error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def cost(
    profile: str | None = typer.Option(None, help="AWS CLI profile name"),
    region: str = typer.Option(DEFAULT_REGION, help="AWS workload region"),
) -> None:
    """Show AWS cost summary."""
    session = _session(profile, region)
    identity = get_identity(session)
    show_header(identity["account"], region, identity["arn"])
    show_cost_summary(get_cost_summary(session))


@app.command()
def credit(
    profile: str | None = typer.Option(None, help="AWS CLI profile name"),
    region: str = typer.Option(DEFAULT_REGION, help="AWS workload region"),
) -> None:
    """Show AWS promotional credit information when permitted."""
    session = _session(profile, region)
    identity = get_identity(session)
    show_header(identity["account"], region, identity["arn"])
    show_credits(get_credits(session, identity["account"]))


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

    show_findings(findings)
    show_recommendations(findings)


if __name__ == "__main__":
    app()
