from __future__ import annotations

import boto3

from aws_costlens_tool.aws.ec2 import list_volumes
from aws_costlens_tool.models.finding import Finding


def check_unattached_ebs(session: boto3.Session, region: str) -> list[Finding]:
    findings: list[Finding] = []

    for volume in list_volumes(session, region):
        if volume.get("State") != "available":
            continue

        volume_id = volume["VolumeId"]
        findings.append(
            Finding(
                category="waste",
                resource_type="EBSVolume",
                resource_id=volume_id,
                title=f"Unattached EBS volume {volume_id}",
                severity="MEDIUM",
                region=region,
                evidence={
                    "size_gib": volume.get("Size"),
                    "volume_type": volume.get("VolumeType"),
                    "state": volume.get("State"),
                    "create_time": str(volume.get("CreateTime")),
                    "encrypted": volume.get("Encrypted"),
                },
                recommendation=(
                    "Review snapshots, ownership, and recovery requirements. Delete only after confirming the volume is no longer required."
                ),
            )
        )

    return findings
