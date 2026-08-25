from botocore.exceptions import ClientError


def _normalize_tags(tags):
    """Convert AWS tags to a dictionary and ignore AWS-managed tags."""
    if not tags:
        return {}

    if isinstance(tags, dict):
        items = tags.items()
    else:
        items = (
            (tag.get("Key"), tag.get("Value", ""))
            for tag in tags
            if isinstance(tag, dict)
        )

    ignored_prefixes = (
        "aws:",
        "eks:",
        "kubernetes.io/",
        "k8s.io/",
    )

    return {
        str(key): str(value or "")
        for key, value in items
        if key
        and not str(key).startswith(ignored_prefixes)
    }


def _record(service, resource, tags):
    tags = _normalize_tags(tags)

    return {
        "service": service,
        "resource": resource,
        "status": "TAGGED" if tags else "UNTAGGED",
        "tags": tags,
    }


def _scan_ec2(session, region):
    client = session.client("ec2", region_name=region)
    records = []

    paginator = client.get_paginator("describe_instances")

    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                records.append(
                    _record(
                        "EC2",
                        instance["InstanceId"],
                        instance.get("Tags", []),
                    )
                )

    return records


def _scan_rds(session, region):
    client = session.client("rds", region_name=region)
    records = []

    paginator = client.get_paginator("describe_db_instances")

    for page in paginator.paginate():
        for database in page.get("DBInstances", []):
            arn = database["DBInstanceArn"]

            tags = client.list_tags_for_resource(
                ResourceName=arn
            ).get("TagList", [])

            records.append(
                _record(
                    "RDS",
                    database["DBInstanceIdentifier"],
                    tags,
                )
            )

    return records


def _scan_s3(session, region):
    client = session.client("s3")
    records = []

    for bucket in client.list_buckets().get("Buckets", []):
        bucket_name = bucket["Name"]

        location = client.get_bucket_location(
            Bucket=bucket_name
        ).get("LocationConstraint")

        bucket_region = location or "us-east-1"

        if bucket_region == "EU":
            bucket_region = "eu-west-1"

        # 현재 CostLens가 검사하는 리전의 S3만 표시
        if bucket_region != region:
            continue

        try:
            tags = client.get_bucket_tagging(
                Bucket=bucket_name
            ).get("TagSet", [])

        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code")

            if code in ("NoSuchTagSet", "NoSuchTagSetError"):
                tags = []
            else:
                raise

        records.append(
            _record(
                "S3",
                bucket_name,
                tags,
            )
        )

    return records


def scan_resource_tags(session, region):
    """Scan EC2, RDS and S3 tagging status."""
    records = []
    errors = []

    scanners = (
        _scan_ec2,
        _scan_rds,
        _scan_s3,
    )

    for scanner in scanners:
        try:
            records.extend(scanner(session, region))
        except ClientError as exc:
            service = scanner.__name__.replace("_scan_", "").upper()
            errors.append(f"{service}: {exc}")

    records.sort(
        key=lambda item: (
            item["service"],
            item["resource"],
        )
    )

    return records, errors
