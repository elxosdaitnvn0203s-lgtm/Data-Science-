import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Contract Risk Assessment Bot",
    layout="centered"
)

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align:center;'>📄 Contract Risk Assessment Bot</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:gray;'>Analyze employment contracts and identify risky clauses easily</p>",
    unsafe_allow_html=True
)

# ---------------- INPUT ----------------
contract_text = st.text_area(
    "Paste Employment Contract Text",
    height=220,
    placeholder="Paste employment contract text here..."
)

# ---------------- FUNCTIONS ----------------
def extract_clauses(text):
    clauses = text.split(".")
    return [c.strip() for c in clauses if c.strip()]

def detect_risk(clause):
    clause = clause.lower()
    if "terminate" in clause or "termination" in clause:
        return "High"
    elif "penalty" in clause or "fine" in clause:
        return "Medium"
    elif "non-compete" in clause or "competitor" in clause:
        return "High"
    else:
        return "Low"

def risk_score(risk):
    if risk == "High":
        return 3
    elif risk == "Medium":
        return 2
    else:
        return 1

def explain_risk(risk):
    if risk == "High":
        return "This clause may be risky and needs careful review."
    elif risk == "Medium":
        return "This clause may cause issues in some situations."
    else:
        return "This clause is generally safe."

# ---------------- ANALYSIS ----------------
if st.button("Analyze Contract"):
    if contract_text.strip() == "":
        st.warning("Please paste contract text before analyzing.")
    else:
        clauses = extract_clauses(contract_text)

        risks = []
        total_score = 0

        for clause in clauses:
            r = detect_risk(clause)
            risks.append(r)
            total_score += risk_score(r)

        # ---------------- SUMMARY CARD ----------------
        st.subheader("📌 Contract Summary")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Clauses", len(clauses))
        col2.metric("High Risk", risks.count("High"))
        col3.metric("Medium Risk", risks.count("Medium"))
        col4.metric("Low Risk", risks.count("Low"))

        # ---------------- RISK CHART ----------------
        st.subheader("📊 Risk Distribution")

        risk_df = pd.DataFrame({
            "Risk Level": ["High", "Medium", "Low"],
            "Count": [
                risks.count("High"),
                risks.count("Medium"),
                risks.count("Low")
            ]
        })

        st.bar_chart(risk_df.set_index("Risk Level"))

        # ---------------- CLAUSE DETAILS ----------------
        st.subheader("📑 Clause Analysis")

        for i, clause in enumerate(clauses):
            risk = detect_risk(clause)
            st.markdown(f"""
            <div style="background-color:#ffffff;padding:15px;border-radius:8px;
                        margin-bottom:10px;border-left:6px solid
                        {'red' if risk=='High' else 'orange' if risk=='Medium' else 'green'};">
                <b>Clause {i+1}:</b> {clause}<br>
                <b>Risk Level:</b> {risk}<br>
                <i>{explain_risk(risk)}</i>
            </div>
            """, unsafe_allow_html=True)

        # ---------------- OVERALL RISK ----------------
        st.subheader("📈 Overall Risk Assessment")
        st.write("**Total Risk Score:**", total_score)

        if total_score <= 5:
            st.success("Overall Contract Risk: LOW")
        elif total_score <= 10:
            st.warning("Overall Contract Risk: MEDIUM")
        else:
            st.error("Overall Contract Risk: HIGH")

        st.caption("⚠️ Note: This is a decision-support tool, not legal advice.")