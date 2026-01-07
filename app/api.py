from fastapi import FastAPI, Query
from app.state import LoanApplicationState
from app.langgraph_agent import build_fast_graph, build_explained_graph

app = FastAPI(
    title="Loan Eligibility AI Agent",
    version="1.0.0"
)

@app.post("/check-eligibility")
def check_eligibility(
    application: LoanApplicationState,
    explain: bool = False
):
    try:
        # Choose graph based on request
        graph = build_explained_graph() if explain else build_fast_graph()

        final_state_dict = graph.invoke(application)
        final_state = LoanApplicationState(**final_state_dict)

        return {
            "verdict": final_state.final_verdict,
            "eligibility_score": final_state.eligibility_score,
            "failed_checks": final_state.failed_checks,
            "explanation": final_state.summary if explain else None,
            "decision_trace": final_state.decision_trace,
        }

    except Exception as e:
        return {
            "verdict": "ERROR",
            "eligibility_score": None,
            "failed_checks": ["System error during evaluation"],
            "explanation": str(e),
        }
