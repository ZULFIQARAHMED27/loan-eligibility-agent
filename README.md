# Explainable Loan Eligibility System with Agentic Orchestration

This project implements an explainable loan eligibility system using a deterministic rule-based decision engine orchestrated via LangGraph.

## Key Features
- Rule-based loan eligibility evaluation
- Agentic orchestration using LangGraph
- Transparent decision trace (audit log)
- Optional LLM-assisted explanation (guarded against hallucination)
- Streamlit frontend for user interaction
- FastAPI backend for API access

## Architecture Overview
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Agent Orchestration:** LangGraph
- **Decision Logic:** Deterministic rule engine
- **AI Explanation:** Local LLM via Ollama (optional)

The AI component is strictly limited to explanation generation and does not influence eligibility decisions.

## How to Run Locally

### Backend
```bash
uvicorn app.api:app --host 127.0.0.1 --port 8000

### Frontend
python -m streamlit run frontend.py

Disclaimer - 
This project is for demonstration purposes only and does not represent real lending policies.