from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LoanApplicationState:
    user_id: str

    kyc_verified: bool
    age: int

    annual_income: float
    monthly_income: float
    total_monthly_emi: float

    credit_score: int
    recent_default: bool

    failed_checks: List[str] = field(default_factory=list)
    eligibility_score: Optional[float] = None
    final_verdict: Optional[str] = None
    summary: Optional[str] = None
    decision_trace: List[dict] = field(default_factory=list)


