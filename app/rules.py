from app.config import ELIGIBILITY_CONFIG
from app.state import LoanApplicationState


def check_kyc(state: LoanApplicationState):
    if not state.kyc_verified:
        state.failed_checks.append("KYC not verified")


def check_age(state: LoanApplicationState):
    if not (ELIGIBILITY_CONFIG["min_age"] <= state.age <= ELIGIBILITY_CONFIG["max_age"]):
        state.failed_checks.append("Age not in eligible range")


def check_income(state: LoanApplicationState):
    if state.annual_income < ELIGIBILITY_CONFIG["min_annual_income"]:
        state.failed_checks.append("Income below threshold")


def check_credit_score(state: LoanApplicationState):
    if state.credit_score < ELIGIBILITY_CONFIG["min_credit_score"]:
        state.failed_checks.append("Credit score below cutoff")


def check_dti(state: LoanApplicationState):
    dti = state.total_monthly_emi / state.monthly_income
    if dti > ELIGIBILITY_CONFIG["max_dti"]:
        state.failed_checks.append("Debt-to-Income ratio too high")


def check_recent_default(state: LoanApplicationState):
    if state.recent_default:
        state.failed_checks.append("Recent default detected")
