import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/check-eligibility"

st.set_page_config(page_title="Loan Eligibility Checker", layout="centered")

st.title("🏦 Loan Eligibility Checker")

st.markdown(
    """
    <div style="
        font-size: 1.1rem;
        font-weight: 600;
        color: #2563eb;
        margin-top: -10px;
        margin-bottom: 20px;
    ">
        • Loan Eligibility System with "Agentic" Orchestration and LLM Assistance 
        • Powered by "LangGraph"
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("ℹ️ How this works"):
    st.write(
        "This tool uses a rule-based decision engine to evaluate loan eligibility "
        "and an AI model to explain the outcome in simple terms. "
        "AI never makes approval decisions — it only explains them."
    )

st.write("Enter your details below to check loan eligibility.")

with st.form("loan_form"):
    user_id = st.text_input("User ID", value="USER001")

    kyc_verified = st.checkbox("KYC Verified")

    age = st.number_input("Age", min_value=18, max_value=100, value=30)

    annual_income = st.number_input("Annual Income (₹)", min_value=0, value=600000)
    monthly_income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
    total_monthly_emi = st.number_input("Total Monthly EMI (₹)", min_value=0, value=15000)

    credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=720)

    recent_default = st.checkbox(
    "Any recent loan default?",
    help="Select YES if you missed EMIs or defaulted on a loan/credit card in the last 12–24 months."
)

    generate_explanation = st.checkbox("Generate AI Explanation (may take a little longer)")

    submit = st.form_submit_button("Check Eligibility")

if submit:
    payload = {
        "user_id": user_id,
        "kyc_verified": kyc_verified,
        "age": age,
        "annual_income": annual_income,
        "monthly_income": monthly_income,
        "total_monthly_emi": total_monthly_emi,
        "credit_score": credit_score,
        "recent_default": recent_default,
    }

    spinner_text = (
        "Evaluating eligibility..."
        if not generate_explanation
        else "Evaluating eligibility and generating explanation..."
    )

    with st.spinner(spinner_text):
        response = requests.post(
            API_URL,
            params={"explain": generate_explanation},
            json=payload,
            timeout=120
        )

    # 👇 EVERYTHING that uses `result` MUST be inside this block
    if response.status_code == 200:
        result = response.json()

        # ---------- FAST RESULT (INSTANT) ----------
        st.subheader("📋 Eligibility Result")

        col1, col2 = st.columns(2)
        col1.metric("Verdict", result["verdict"])
        col2.metric("Eligibility Score", result["eligibility_score"])

        if result["failed_checks"]:
            st.error("❌ Failed Checks")
            for reason in result["failed_checks"]:
                st.write(f"- {reason}")
        else:
            st.success("✅ All eligibility checks passed")

        # ---------- DECISION TRACE (AUDIT LOG) ----------
        st.subheader("🧾 Decision Trace")

        for item in result["decision_trace"]:
            status_icon = "✅" if item["status"] == "PASS" else "❌"
            st.write(f"{status_icon} **{item['check']}**")


        # ---------- SLOW PART (OPTIONAL AI EXPLANATION) ----------
        if generate_explanation:
            st.subheader("🧠 AI Explanation")
            for line in result["explanation"].split("\n"):
             st.write(line)



    else:
        st.error("❌ Backend returned an error")
        st.write("Status code:", response.status_code)
        st.write("Response:", response.text)
