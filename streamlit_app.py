import streamlit as st
import pandas as pd

st.set_page_config(page_title="InsightAI – Your AI Business Analyst")

st.title("🧠 InsightAI – Your AI Business Analyst")
st.markdown("Upload your CSV or Excel file")

uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📊 Uploaded Data Preview")
        st.dataframe(df)

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
