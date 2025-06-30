import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from fpdf import FPDF
import os

# Page settings
st.set_page_config(
    page_title="InsightAI - Business Data Analyst",
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
    <div class='subtitle'>Built with Streamlit (No AI)</div>
    <hr style="margin-top:10px; margin-bottom:20px;">
""", unsafe_allow_html=True)

st.markdown("Upload your CSV or Excel file, explore insights, generate charts, and download reports.")

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

        # PDF Report Download (only stats)
        st.subheader("📄 Download Data Report")
        if st.button("Generate & Download PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "InsightAI - Business Data Report", ln=True, align="C")
            pdf.ln(10)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, f"Summary Statistics:\n{df.describe().to_string()}")

            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            buffer = BytesIO(pdf_bytes)
            st.download_button("Download Report PDF", buffer, file_name="InsightAI_Report.pdf", mime="application/pdf")

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
else:
    st.info("Please upload a CSV or Excel file to get started.")

# Download CSV log file (optional — can remove if not needed)
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
    st.info("No log file yet.")

# Footer
st.markdown("""
    <hr>
    <center>
    <span style="font-size:13px">Made with ❤️ by Sagar • GitHub: <a href="https://github.com/sagar5282" target="_blank">sagar5282</a></span>
    </center>
""", unsafe_allow_html=True)
