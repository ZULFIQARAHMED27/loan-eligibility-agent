from app.state import LoanApplicationState
from app.rules import (
    check_kyc,
    check_age,
    check_income,
    check_credit_score,
    check_dti,
    check_recent_default,
)


def calculate_eligibility_score(state: LoanApplicationState) -> float:
    score = 0

    # Credit score (max 40)
    if state.credit_score >= 750:
        score += 40
    elif state.credit_score >= 700:
        score += 30
    elif state.credit_score >= 650:
        score += 20

    # Income strength (max 25)
    if state.annual_income >= 800000:
        score += 25
    elif state.annual_income >= 500000:
        score += 18
    else:
        score += 10

    # DTI health (max 25)
    dti = state.total_monthly_emi / state.monthly_income
    if dti <= 0.25:
        score += 25
    elif dti <= 0.35:
        score += 15
    elif dti <= 0.40:
        score += 5

    # Stability bonus (max 10)
    if not state.recent_default:
        score += 10

    return score


def run_eligibility_checks(state):
    failed_checks = []
    score = 0
    trace = []

    # KYC
    if state.kyc_verified:
        score += 15
        trace.append({"check": "KYC Verification", "status": "PASS"})
    else:
        failed_checks.append("KYC not verified")
        trace.append({"check": "KYC Verification", "status": "FAIL"})

    # Age
    if 21 <= state.age <= 60:
        score += 15
        trace.append({"check": "Age Eligibility", "status": "PASS"})
    else:
        failed_checks.append("Age not within allowed range")
        trace.append({"check": "Age Eligibility", "status": "FAIL"})

    # Income
    if state.annual_income >= 300000:
        score += 15
        trace.append({"check": "Income Threshold", "status": "PASS"})
    else:
        failed_checks.append("Income below threshold")
        trace.append({"check": "Income Threshold", "status": "FAIL"})

    # Credit score
    if state.credit_score >= 700:
        score += 20
        trace.append({"check": "Credit Score", "status": "PASS"})
    else:
        failed_checks.append("Low credit score")
        trace.append({"check": "Credit Score", "status": "FAIL"})

    # Debt-to-income
    dti = state.total_monthly_emi / max(state.monthly_income, 1)
    if dti <= 0.4:
        score += 15
        trace.append({"check": "Debt-to-Income Ratio", "status": "PASS"})
    else:
        failed_checks.append("Debt-to-Income ratio too high")
        trace.append({"check": "Debt-to-Income Ratio", "status": "FAIL"})

    # Recent default
    if not state.recent_default:
        score += 20
        trace.append({"check": "Recent Loan Default", "status": "PASS"})
    else:
        failed_checks.append("Recent loan default detected")
        trace.append({"check": "Recent Loan Default", "status": "FAIL"})

    state.eligibility_score = score
    state.failed_checks = failed_checks
    state.decision_trace = trace
    state.final_verdict = "APPROVED" if not failed_checks else "REJECTED"

    return state

