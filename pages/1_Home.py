import streamlit as st
import pandas as pd

st.title("📂 Home - Upload & Preview")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.session_state["df"] = df
    st.subheader("📊 Preview")
    st.dataframe(df.head())
