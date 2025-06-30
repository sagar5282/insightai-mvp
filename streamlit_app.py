import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
import seaborn as sns

# Page settings
st.set_page_config(page_title="InsightAI – Your AI Business Analyst", layout="wide")

st.title("🧠 InsightAI – Your AI Business Analyst")
st.markdown("Upload your CSV or Excel file and ask questions using AI.")

# Upload file
uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📊 Uploaded Data Preview")
        st.dataframe(df)

        st.subheader("📈 Summary Statistics")
        st.write(df.describe())

        # AI Question
        st.subheader("💬 Ask InsightAI")
        user_question = st.text_input("Ask a question about your data (e.g., Which region has highest sales?)")

        if user_question:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            sample_data = df.head(10).to_string()
            prompt = (
                f"Dataset sample:\n{sample_data}\n\n"
                f"User question: {user_question}\n\n"
                "Please provide a detailed answer in simple business terms."
            )
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "You are a skilled business data analyst."},
                          {"role": "user", "content": prompt}]
            )
            answer = response["choices"][0]["message"]["content"]
            st.markdown("### 🤖 InsightAI Answer")
            st.write(answer)

        # Optional: Show column-wise plot
        st.subheader("📊 Quick Visualization")
        if st.checkbox("Show column distribution plot"):
            numeric_cols = df.select_dtypes(include=['float', 'int']).columns
            if len(numeric_cols) > 0:
                selected_col = st.selectbox("Select a numeric column", numeric_cols)
                fig, ax = plt.subplots()
                sns.histplot(df[selected_col], kde=True, ax=ax)
                st.pyplot(fig)
            else:
                st.info("No numeric columns found for plotting.")

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
