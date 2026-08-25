from aws_costlens_tool.models.finding import Finding


def test_finding_model() -> None:
    finding = Finding(
        category="waste",
        resource_type="ElasticIP",
        resource_id="eipalloc-123",
        title="Unassociated Elastic IP",
        severity="MEDIUM",
        region="ap-northeast-2",
        recommendation="Review and release if unused.",
        estimated_monthly_cost_usd=3.65,
    )

    assert finding.resource_type == "ElasticIP"
    assert finding.estimated_monthly_cost_usd == 3.65
