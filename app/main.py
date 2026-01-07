from app.state import LoanApplicationState
from app.langgraph_agent import build_loan_eligibility_graph


if __name__ == "__main__":
    graph = build_loan_eligibility_graph()

    application = LoanApplicationState(
        user_id="DEMO_USER",
        kyc_verified=True,
        age=30,
        annual_income=600000,
        monthly_income=50000,
        total_monthly_emi=15000,
        credit_score=720,
        recent_default=False
    )

    final_state_dict = graph.invoke(application)
    final_state = LoanApplicationState(**final_state_dict)

    print("Final Verdict:", final_state.final_verdict)
    print("Eligibility Score:", final_state.eligibility_score)
    print("Failed Checks:", final_state.failed_checks)
    print("\n--- AI Explanation (LangGraph + Mistral) ---")
    print(final_state.summary)
