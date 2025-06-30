import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="InsightAI", layout="wide")
st.title("🧠 InsightAI – Your AI Business Analyst")

uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    st.subheader("📈 Summary Stats")
    st.write(df.describe())

    st.subheader("💬 Ask InsightAI")
    user_question = st.text_input("Ask a question about your data:")
    
    if user_question:
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        prompt = f"Analyze the following data:\n{df.head(10).to_string()}\n\nQuestion: {user_question}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write(response["choices"][0]["message"]["content"])
