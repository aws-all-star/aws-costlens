from __future__ import annotations

import boto3


def list_addresses(session: boto3.Session, region: str) -> list[dict]:
    ec2 = session.client("ec2", region_name=region)
    return ec2.describe_addresses().get("Addresses", [])


def list_volumes(session: boto3.Session, region: str) -> list[dict]:
    ec2 = session.client("ec2", region_name=region)
    paginator = ec2.get_paginator("describe_volumes")
    volumes: list[dict] = []
    for page in paginator.paginate():
        volumes.extend(page.get("Volumes", []))
    return volumes


def list_instances(session: boto3.Session, region: str) -> list[dict]:
    ec2 = session.client("ec2", region_name=region)
    paginator = ec2.get_paginator("describe_instances")
    instances: list[dict] = []
    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            instances.extend(reservation.get("Instances", []))
    return instances
