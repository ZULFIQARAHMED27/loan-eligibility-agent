import json

import os
os.environ["OLLAMA_NO_CUDA"] = "1"

import ollama
from app.state import LoanApplicationState


def generate_explanation(state: LoanApplicationState) -> str:
    system_prompt = (
        "You are a deterministic explanation engine.\n"
        "Your task is to restate given facts without interpretation.\n\n"

        "Rules:\n"
        "- Do NOT explain why something is good or bad\n"
        "- Do NOT infer risk, suitability, or intent\n"
        "- Do NOT interpret scores or numbers\n"
        "- Do NOT introduce new terms\n"
        "- Do NOT use prose paragraphs\n"
        "- Output MUST be valid JSON matching the schema exactly\n"
    )

    user_prompt = {
        "verdict": state.final_verdict,
        "eligibility_score": state.eligibility_score,
        "failed_checks": state.failed_checks,
        "schema": {
            "summary_points": [
                "string (fact copied from input only)"
            ]
        }
    }

    try:
        response = ollama.chat(
            model="mistral:7b-instruct-q4_K_M",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt)},
            ],
        )

        raw = response["message"]["content"]

        # 🔒 HARD VALIDATION LAYER
        parsed = json.loads(raw)

        points = parsed.get("summary_points", [])

        # Reject hallucination by rule
        safe_points = []
        for p in points:
            if any(x in p.lower() for x in ["risk", "lender", "decile", "protocol", "suitable"]):
                continue
            safe_points.append(p)

        if not safe_points:
            raise ValueError("Invalid explanation content")

        return "\n".join(f"• {p}" for p in safe_points)

    except Exception:
        if not state.failed_checks:
            return "\n".join([
            "• The loan eligibility decision was approved.",
            "• All required eligibility checks were evaluated.",
            "• No eligibility checks failed during evaluation.",
            f"• The final eligibility score was {state.eligibility_score}.",
            "• The decision was made using predefined rules without AI influence."
        ])
        else:
            return "\n".join([
            "• The loan eligibility decision was not approved.",
            "• One or more eligibility checks failed during evaluation.",
            f"• Failed checks: {', '.join(state.failed_checks)}",
            f"• The final eligibility score was {state.eligibility_score}.",
            "• The decision was made using predefined rules without AI influence."
        ])

