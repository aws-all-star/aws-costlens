from unittest.mock import patch

from aws_costlens_tool.checks.eip import check_unassociated_eips


@patch("aws_costlens_tool.checks.eip.list_addresses")
def test_unassociated_eip_is_reported(mock_list_addresses) -> None:
    mock_list_addresses.return_value = [
        {
            "PublicIp": "203.0.113.10",
            "AllocationId": "eipalloc-test",
        }
    ]

    findings = check_unassociated_eips(session=object(), region="ap-northeast-2")

    assert len(findings) == 1
    assert findings[0].resource_id == "eipalloc-test"
    assert findings[0].estimated_monthly_cost_usd == 3.65
