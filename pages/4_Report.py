import streamlit as st
from fpdf import FPDF
from io import BytesIO

st.title("📄 Report Download")

if "df" not in st.session_state or "ai_answer" not in st.session_state:
    st.warning("Please upload data and ask a question first.")
else:
    df = st.session_state["df"]
    answer = st.session_state["ai_answer"]
    question = st.session_state["ai_question"]

    if st.button("Generate PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"InsightAI Report\n\nQuestion:\n{question}\n\nAnswer:\n{answer}\n\nStats:\n{df.describe().to_string()}")

        buf = BytesIO()
        pdf.output(buf)
        buf.seek(0)
        st.download_button("Download PDF", buf, file_name="insightai_report.pdf", mime="application/pdf")
