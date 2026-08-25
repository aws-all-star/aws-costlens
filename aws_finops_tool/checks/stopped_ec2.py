from __future__ import annotations

import boto3

from aws_finops_tool.aws.ec2 import list_instances
from aws_finops_tool.models.finding import Finding


def check_stopped_instances(session: boto3.Session, region: str) -> list[Finding]:
    findings: list[Finding] = []

    for instance in list_instances(session, region):
        state = instance.get("State", {}).get("Name")
        if state != "stopped":
            continue

        instance_id = instance["InstanceId"]
        name = _tag(instance, "Name") or instance_id
        findings.append(
            Finding(
                category="review",
                resource_type="EC2Instance",
                resource_id=instance_id,
                title=f"Stopped EC2 instance {name}",
                severity="LOW",
                region=region,
                evidence={
                    "instance_type": instance.get("InstanceType"),
                    "state": state,
                    "name": name,
                },
                recommendation=(
                    "Confirm whether the instance is still needed. Review attached EBS volumes and Elastic IPs before cleanup."
                ),
            )
        )

    return findings


def _tag(instance: dict, key: str) -> str | None:
    for tag in instance.get("Tags", []):
        if tag.get("Key") == key:
            return tag.get("Value")
    return None
