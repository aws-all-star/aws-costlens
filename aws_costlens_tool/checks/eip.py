from __future__ import annotations

import boto3

from aws_costlens_tool.aws.ec2 import list_addresses
from aws_costlens_tool.config import EIP_HOURLY_PUBLIC_IPV4_USD, HOURS_PER_MONTH
from aws_costlens_tool.models.finding import Finding


def check_unassociated_eips(session: boto3.Session, region: str) -> list[Finding]:
    findings: list[Finding] = []
    monthly_cost = EIP_HOURLY_PUBLIC_IPV4_USD * HOURS_PER_MONTH

    for address in list_addresses(session, region):
        if address.get("AssociationId"):
            continue

        allocation_id = address.get("AllocationId", "unknown")
        public_ip = address.get("PublicIp", "unknown")
        findings.append(
            Finding(
                category="waste",
                resource_type="ElasticIP",
                resource_id=allocation_id,
                title=f"Unassociated Elastic IP {public_ip}",
                severity="MEDIUM",
                region=region,
                estimated_monthly_cost_usd=monthly_cost,
                evidence={
                    "public_ip": public_ip,
                    "allocation_id": allocation_id,
                    "association_id": address.get("AssociationId"),
                },
                recommendation=(
                    "Verify DNS, firewall allowlists, and dependencies. If unused, release the Elastic IP."
                ),
            )
        )

    return findings
