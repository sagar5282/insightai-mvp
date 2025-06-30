import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from fpdf import FPDF
import csv
import datetime
import os

# Page settings
st.set_page_config(
    page_title="InsightAI - AI Business Analyst",
    page_icon="📊",
    layout="wide"
)

# Custom header
st.markdown("""
    <style>
        .big-title {
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
        }
        .subtitle {
            font-size: 18px;
            color: gray;
        }
    </style>
    <div class='big-title'>📊 InsightAI – Your Smart Business Data Analyst</div>
    <div class='subtitle'>Powered by GPT-4 • Built with Streamlit</div>
    <hr style="margin-top:10px; margin-bottom:20px;">
""", unsafe_allow_html=True)

st.markdown("Upload your CSV or Excel file, explore insights, generate charts, download reports, and manage logs.")

# Upload file
uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📊 Uploaded Data Preview")
        st.dataframe(df)

        st.subheader("📈 Summary Statistics")
        st.write(df.describe())

        # Ask AI
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

            # 💾 Save to CSV log
            log_filename = "insightai_logs.csv"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(log_filename, mode="a", newline="", encoding="utf-8") as log_file:
                writer = csv.writer(log_file)
                writer.writerow([timestamp, user_question, answer])

        # Auto Chart Section
        st.subheader("📊 Auto Chart Builder")

        numeric_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()

        if numeric_cols:
            chart_type = st.selectbox("Select chart type", ["Histogram", "Bar Plot"])
            num_col = st.selectbox("Select numeric column", numeric_cols)

            if chart_type == "Histogram":
                fig, ax = plt.subplots()
                sns.histplot(df[num_col], kde=True, ax=ax)
                st.pyplot(fig)

            elif chart_type == "Bar Plot" and cat_cols:
                cat_col = st.selectbox("Select categorical column (Group By)", cat_cols)
                fig, ax = plt.subplots()
                grouped_df = df.groupby(cat_col)[num_col].mean().reset_index()
                sns.barplot(x=cat_col, y=num_col, data=grouped_df, ax=ax)
                st.pyplot(fig)
        else:
            st.info("No numeric columns found to create charts.")

        # PDF Report Download
        st.subheader("📄 Download AI Insights Report")
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
else:
    st.info("Please upload a CSV or Excel file to get started.")

# Download CSV log file
st.subheader("⬇️ Download Logs CSV")
if os.path.exists("insightai_logs.csv"):
    with open("insightai_logs.csv", "rb") as f:
        st.download_button(
            label="Download Logs CSV",
            data=f,
            file_name="insightai_logs.csv",
            mime="text/csv"
        )
else:
    st.info("No log file yet. Logs will appear here after first question.")

# Footer
st.markdown("""
    <hr>
    <center>
    <span style="font-size:13px">Made with ❤️ by Sagar • GitHub: <a href="https://github.com/sagar5282" target="_blank">sagar5282</a></span>
    </center>
""", unsafe_allow_html=True)
