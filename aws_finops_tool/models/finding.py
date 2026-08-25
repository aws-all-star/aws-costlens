from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Finding:
    category: str
    resource_type: str
    resource_id: str
    title: str
    severity: str
    region: str
    recommendation: str
    estimated_monthly_cost_usd: float | None = None
    evidence: dict[str, Any] = field(default_factory=dict)
