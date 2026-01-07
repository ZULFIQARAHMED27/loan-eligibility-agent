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

Rules Explained

KYC Verification

Applicant must be KYC verified

Mandatory gating rule

Age Eligibility

Age must be between 21 and 60

Income Threshold

Annual income must meet minimum threshold

Credit Score Check

Credit score must meet minimum cutoff

Debt-to-Income Ratio (DTI)

Monthly EMI / Monthly Income ≤ 40%

Recent Loan Default

No loan or credit card default within last 24 months

🧾 Decision Trace (Explainability by Design)

For every evaluation, the system produces a decision trace:

[
  {"check": "KYC Verification", "status": "PASS"},
  {"check": "Age Eligibility", "status": "PASS"},
  {"check": "Income Threshold", "status": "PASS"},
  {"check": "Credit Score", "status": "PASS"},
  {"check": "Debt-to-Income Ratio", "status": "PASS"},
  {"check": "Recent Loan Default", "status": "PASS"}
]

This trace ensures:

Full transparency

Auditability

No reliance on AI explanations for correctness

🤖 Why the AI Explanation Feels “Template-like”

This is intentional.

Key Design Choice

The LLM is not allowed to interpret, infer, or justify decisions.

Why?

Free-form explanations hallucinate

Financial explanations must be verifiable

Regulators require deterministic reasoning

How this is handled

LLM is constrained to structured JSON output

Only allowed to restate known system facts

Hard validation rejects invented language

Deterministic fallback used if LLM misbehaves

This results in boring but correct explanations, which is the desired outcome in this domain.

🧠 Is This an AI Agent?
Honest Answer

This is not a fully autonomous AI agent.

What it is

A hybrid agentic system

Deterministic decision core

Agentic orchestration layer

LLM-assisted explanation module

Where it aligns with AI Agent architecture

Explicit agent state

Conditional execution

Tool isolation

Separation of concerns

Orchestration via LangGraph

Why full autonomy was avoided

Loan decisions must be auditable

Autonomous policy reasoning is risky

Learned behavior is often disallowed in finance

This reflects real-world production constraints, not a limitation.

🛠️ Setup & Run Instructions (Step-by-Step)
1. Clone the Repository
git clone <repo-url>
cd loan-eligibility-agent

2. Create Virtual Environment
python -m venv .venv

3. Activate Virtual Environment

Windows

.\.venv\Scripts\Activate.ps1


Linux / macOS

source .venv/bin/activate

4. Install Dependencies
pip install -r requirements.txt

5. Run Backend (FastAPI)
uvicorn app.api:app --host 127.0.0.1 --port 8000


Optional:

Open http://127.0.0.1:8000/docs to test API

6. Run Frontend (Streamlit)
python -m streamlit run frontend.py

⚠️ Key Challenges & How They Were Solved
1. Hallucination in Explanations

Solved using schema-constrained output

Removed free-form reasoning

Added validation + fallback logic

2. Mixing Rules with LLM

Separated decision authority from explanation

LangGraph used to enforce boundaries

3. Explainability vs Overclaiming AI

Explicitly avoided calling this an autonomous agent

Documented design tradeoffs clearly

4. UI Formatting of Generated Text

Streamlit rendering issues fixed via line-by-line rendering

Avoided Markdown ambiguity

📌 Use Cases

Fintech eligibility pre-check systems

Internal underwriting tools

Explainable decision demos

Agentic system architecture reference

Interview / portfolio project for AI engineers

🚫 Disclaimer

This project is for demonstration and educational purposes only.
It does not represent real lending policies or financial advice.

🧠 Final Notes

This project intentionally prioritizes:

correctness over cleverness

transparency over autonomy

safety over hype

The architecture reflects how real-world AI systems are actually built in regulated domains.
