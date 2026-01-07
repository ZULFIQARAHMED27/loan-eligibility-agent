from langgraph.graph import StateGraph, END
from app.state import LoanApplicationState
from app.eligibility_engine import run_eligibility_checks
from app.explanation_agent import generate_explanation


def eligibility_node(state: LoanApplicationState) -> LoanApplicationState:
    return run_eligibility_checks(state)


def explanation_node(state: LoanApplicationState) -> LoanApplicationState:
    state.summary = generate_explanation(state)
    return state


def build_fast_graph():
    """
    Eligibility-only graph (NO LLM)
    """
    graph = StateGraph(LoanApplicationState)
    graph.add_node("eligibility", eligibility_node)
    graph.set_entry_point("eligibility")
    graph.add_edge("eligibility", END)
    return graph.compile()


def build_explained_graph():
    """
    Eligibility + Explanation graph (uses LLM)
    """
    graph = StateGraph(LoanApplicationState)
    graph.add_node("eligibility", eligibility_node)
    graph.add_node("explanation", explanation_node)
    graph.set_entry_point("eligibility")
    graph.add_edge("eligibility", "explanation")
    graph.add_edge("explanation", END)
    return graph.compile()