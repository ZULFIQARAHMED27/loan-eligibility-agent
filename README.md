# Explainable Loan Eligibility System with Agentic Orchestration

This project implements an **explainable loan eligibility system** using a **deterministic, rule-based decision engine** orchestrated through **agentic control flow** via LangGraph, with **guarded LLM-assisted explanations**.

The system is intentionally designed to balance:
- correctness and auditability (core decision logic)
- agentic orchestration (stateful execution)
- safe, non-hallucinatory AI usage (explanation only)

This is **not a fully autonomous AI agent by design**, especially because the financial domain requires deterministic, traceable decisions.

---

## 🧠 High-Level Overview

**What this system does**
- Accepts loan applicant inputs (KYC, income, credit score, etc.)
- Evaluates eligibility using predefined business rules
- Produces:
  - final verdict (APPROVED / REJECTED)
  - eligibility score
  - detailed decision trace (audit log)
  - optional AI-generated explanation (guarded)

**What this system does NOT do**
- It does NOT let an LLM decide loan approvals
- It does NOT learn or adapt thresholds automatically
- It does NOT make probabilistic or opaque decisions

This design is **intentional and realistic** for regulated domains.

---

## 🏗️ System Architecture (End-to-End)

### Flow Summary

1. User enters details via Streamlit UI
2. Frontend sends JSON payload to FastAPI backend
3. FastAPI invokes a LangGraph-based agent
4. Agent executes deterministic eligibility rules
5. Decision trace and score are generated
6. Optional explanation is produced using a constrained LLM
7. Final structured response is returned to UI

### Core Principle
> **Decisions are deterministic. AI is only used to explain decisions, not to make them.**

---

## 🧩 Technologies, Tools & Frameworks Used

### Frontend
- **Streamlit**
  - Form-based UI
  - Displays verdict, score, decision trace, explanation
  - Explicit formatting control for generated text

### Backend
- **FastAPI**
  - API layer for eligibility evaluation
  - Input validation via Pydantic
  - Clean separation from UI logic

### Agentic Orchestration
- **LangGraph**
  - Orchestrates execution flow
  - Maintains shared mutable state
  - Separates decision node from explanation node
  - Enables conditional execution paths

### Core Decision Logic
- **Pure Python rule engine**
  - Transparent and deterministic
  - Produces audit-ready decision trace
  - Easy to reason about and test

### AI Explanation Layer
- **Ollama (local LLM runtime)**
- **Mistral 7B (quantized)**
  - Used only for language generation
  - Output constrained to structured schema
  - Guarded against hallucination
  - Fallbacks in place if LLM fails

### Data Modeling
- **LoanApplicationState**
  - Single source of truth
  - Shared across agent nodes
  - Prevents inconsistent or hallucinated state

---

## ⚙️ Eligibility Rules Implemented

All eligibility rules are **explicit, configurable, and deterministic**.

```python
ELIGIBILITY_CONFIG = {
    "min_age": 21,
    "max_age": 60,
    "min_annual_income": 300000,
    "min_credit_score": 650,
    "max_dti": 0.40,
    "default_lookback_months": 24
}
```
✅Eligibility Rules Explained

The loan eligibility decision is based on a fixed set of deterministic rules. Each rule is evaluated independently, and the final verdict is derived from the combined outcome of all checks.

- KYC Verification
The applicant must have completed Know Your Customer (KYC) verification. This is a mandatory gating condition—if KYC is not verified, the application is immediately rejected.

- Age Eligibility
The applicant’s age must fall within an acceptable range, defined as 21 to 60 years. Applications outside this range are considered ineligible.

- Income Threshold
The applicant must meet a minimum annual income requirement. This ensures a baseline repayment capacity before further checks are performed.

- Credit Score Check
The applicant’s credit score must meet or exceed a predefined cutoff. This rule acts as a proxy for historical credit behavior and repayment discipline.

- Debt-to-Income Ratio (DTI)
The system evaluates the ratio of total monthly loan EMIs to monthly income. The application passes this check only if the ratio remains within the acceptable limit, ensuring the applicant is not over-leveraged.

- Recent Loan Default
The applicant must not have any recent loan or credit card defaults within the defined lookback period (e.g., the last 24 months). Any recent default results in rejection.

✅Decision Trace (Explainability by Design)

For every eligibility evaluation, the system produces a decision trace.
This trace records the outcome of each individual rule check, clearly indicating whether it passed or failed.

The decision trace serves three critical purposes:

- It provides full transparency into how the verdict was reached.

- It enables auditability, making the system suitable for regulated environments.

- It ensures that correctness does not depend on AI-generated explanations.

The decision trace is the authoritative source of truth for the eligibility decision.

✅Why the AI Explanation Feels “Template-like”

- This behavior is intentional and by design.

- Key Design Choice

- The language model is not allowed to interpret, infer, or justify decisions. Its role is limited strictly to restating known system outcomes.

✅Why This Restriction Exists

- Free-form LLM explanations are prone to hallucination.

- Financial decisions require explanations that are verifiable and factual.

- Regulatory and compliance requirements demand deterministic reasoning.

✅How This Is Enforced

- The LLM is constrained to structured output formats.

- It is only allowed to restate facts already present in system state.

- Outputs are validated, and invented or speculative language is rejected.

- A deterministic fallback explanation is used if the LLM fails or misbehaves.

- As a result, explanations may appear repetitive or “template-like,” but they are correct, safe, and auditable, which is the desired outcome in this domain.

✅Is This an AI Agent?
Honest Answer

- This system is not a fully autonomous AI agent.

✅What It Is

- It is a hybrid agentic system consisting of:

- A deterministic decision core

- An agentic orchestration layer

- An LLM-assisted explanation module

✅Where It Aligns with AI Agent Architecture

- Explicit shared agent state

- Conditional execution of steps

- Clear separation of tools and responsibilities

- Separation of concerns between decision logic and explanation

- Execution orchestration implemented using LangGraph

✅Why Full Autonomy Was Avoided

- Loan decisions must be explainable and auditable

- Autonomous policy reasoning introduces risk

- Learned or adaptive behavior is often disallowed in financial systems

- These constraints reflect real-world production requirements, not architectural limitations.

✅Setup and Run Instructions (Step-by-Step)

To run the system locally, follow the steps below.

- First, clone the repository and navigate into the project directory.
- Next, create a Python virtual environment and activate it based on your operating system.
- Once activated, install all required dependencies using the provided requirements file.

✅After setup:

- Start the backend using FastAPI to expose the eligibility API.

- Optionally access the API documentation via the built-in Swagger UI.

- Launch the Streamlit frontend to interact with the system through a user interface.

✅Key Challenges and How They Were Solved

Hallucination in AI Explanations
This was addressed by enforcing schema-constrained outputs, eliminating free-form reasoning, and introducing strict validation with deterministic fallbacks.

Combining Rules with an LLM
Decision authority was strictly separated from explanation generation. LangGraph was used to enforce execution boundaries and state flow.

Explainability Without Overclaiming AI
The system intentionally avoids presenting itself as a fully autonomous agent. Architectural tradeoffs are documented clearly and honestly.

UI Formatting of Generated Text
Streamlit rendering issues were resolved by rendering explanations line-by-line and avoiding ambiguous Markdown formatting.

✅Use Cases

This system can be applied to:

- Fintech loan eligibility pre-check workflows

- Internal underwriting and screening tools

- Explainable decision-making demonstrations

- Reference implementations for agentic system design

- Portfolio projects for AI and GenAI engineering roles

⚠️Disclaimer

This project is for demonstration and educational purposes only.
It does not represent real lending policies or constitute financial advice.

✅Final Notes

This project intentionally prioritizes:

- Correctness over cleverness

- Transparency over autonomy

- Safety over hype

- The architecture reflects how real-world AI systems are built in regulated domains, where explainability and control matter more than unchecked autonomy.
