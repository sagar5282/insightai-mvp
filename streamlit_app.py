import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from fpdf import FPDF

# Page settings
st.set_page_config(page_title="InsightAI – Your AI Business Analyst", layout="wide")

st.title("🧠 InsightAI – Your AI Business Analyst")
st.markdown("Upload your CSV or Excel file, ask questions, and auto-generate insights & charts.")

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

        # 💬 Ask AI
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
                messages=[
                    {"role": "system", "content": "You are a skilled business data analyst."},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response["choices"][0]["message"]["content"]
            st.markdown("### 🤖 InsightAI Answer")
            st.write(answer)

        # 📊 Auto Chart Section
        st.subheader("📊 Quick Auto Chart")

        numeric_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()

        if numeric_cols:
            chart_type = st.selectbox("Select chart type", ["Histogram", "Bar Plot"])
            selected_col = st.selectbox("Select numeric column to plot", numeric_cols)

            if st.button("Generate Chart"):
                fig, ax = plt.subplots()
                if chart_type == "Histogram":
                    sns.histplot(df[selected_col], kde=True, ax=ax)
                else:  # Bar Plot
                    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
                    if cat_cols:
                        cat_col = st.selectbox("Group by (categorical column)", cat_cols, key="cat_col")
                        grouped_df = df.groupby(cat_col)[selected_col].mean().reset_index()
                        sns.barplot(x=cat_col, y=selected_col, data=grouped_df, ax=ax)
                    else:
                        st.warning("No categorical columns found for bar plot grouping.")
                st.pyplot(fig)
        else:
            st.info("No numeric columns found for auto chart.")

        # 📝 Downloadable PDF Report
        st.subheader("📝 Download AI Insights Report")
        if st.button("Generate & Download PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "InsightAI - Business Data Report", ln=True, align="C")
            pdf.ln(10)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, f"Summary Statistics:\n{df.describe().to_string()}")
            if user_question:
                pdf.ln(5)
                pdf.multi_cell(0, 10, f"User Question:\n{user_question}\n\nAI Answer:\n{answer}")

            buffer = BytesIO()
            pdf.output(buffer)
            buffer.seek(0)
            st.download_button("Download Report PDF", buffer, file_name="InsightAI_Report.pdf", mime="application/pdf")

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
