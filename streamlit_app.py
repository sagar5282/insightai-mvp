import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from fpdf import FPDF

# --------------------
# ✅ Page config & header
# --------------------
st.set_page_config(page_title="InsightAI - Business Data Analyst", page_icon="📊", layout="wide")

st.markdown("""
    <style>
        .big-title {font-size: 36px; font-weight: bold; color: #ff6f61;}
        .subtitle {font-size: 18px; color: gray;}
        .stTabs [data-baseweb="tab"] {font-size: 16px; padding: 10px;}
    </style>
    <div class='big-title'>📊 InsightAI – Your Smart Business Data Analyst</div>
    <div class='subtitle'>Visual analysis and insights (No AI)</div>
    <hr style="margin-top:10px; margin-bottom:20px;">
""", unsafe_allow_html=True)

# --------------------
# ✅ Upload data
# --------------------
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.sidebar.success("✅ File uploaded successfully!")

    # Tabs
    tabs = st.tabs(["🏠 Home", "📊 Charts", "💡 Insights", "📄 Report"])

    # --- Home Tab ---
    with tabs[0]:
        st.subheader("📄 Data Preview")
        st.dataframe(df)

        st.subheader("📈 Summary Statistics")
        st.write(df.describe())

        # KPI dashboard
        st.subheader("📊 Executive Dashboard")
        if "Sales" in df.columns and "Profit" in df.columns and "Region" in df.columns:
            total_sales = df["Sales"].sum()
            avg_profit = df["Profit"].mean()
            top_region = df.groupby("Region")["Sales"].sum().idxmax()

            st.metric("Total Sales", f"${total_sales:,.0f}")
            st.metric("Average Profit", f"${avg_profit:,.0f}")
            st.metric("Top Region", top_region)
        else:
            st.info("Upload data with columns: 'Sales', 'Profit', 'Region' for executive KPIs.")

    # --- Charts Tab ---
    with tabs[1]:
        st.subheader("📊 Advanced Charts")

        numeric_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()

        if not numeric_cols:
            st.warning("⚠️ No numeric columns found for plotting.")
        else:
            chart_type = st.selectbox("Choose chart type", ["Histogram", "Bar Plot", "Line Chart", "Pie Chart", "Scatter Plot"])

            fig, ax = plt.subplots()

            if chart_type == "Histogram":
                num_col = st.selectbox("Select numeric column", numeric_cols)
                if num_col:
                    sns.histplot(df[num_col], kde=True, ax=ax)
                    st.pyplot(fig)

            elif chart_type == "Bar Plot":
                if cat_cols:
                    cat_col = st.selectbox("Select categorical column", cat_cols)
                    num_col = st.selectbox("Select numeric column", numeric_cols)
                    if cat_col and num_col:
                        grouped = df.groupby(cat_col)[num_col].mean().reset_index()
                        sns.barplot(x=cat_col, y=num_col, data=grouped, ax=ax)
                        st.pyplot(fig)
                else:
                    st.warning("⚠️ No categorical columns found for Bar Plot.")

            elif chart_type == "Line Chart":
                if cat_cols:
                    cat_col = st.selectbox("Select categorical column", cat_cols)
                    num_col = st.selectbox("Select numeric column", numeric_cols)
                    if cat_col and num_col:
                        grouped = df.groupby(cat_col)[num_col].mean().reset_index()
                        sns.lineplot(x=cat_col, y=num_col, data=grouped, marker="o", ax=ax)
                        st.pyplot(fig)
                else:
                    st.warning("⚠️ No categorical columns found for Line Chart.")

            elif chart_type == "Pie Chart":
                if cat_cols:
                    cat_col = st.selectbox("Select categorical column", cat_cols)
                    num_col = st.selectbox("Select numeric column", numeric_cols)
                    if cat_col and num_col:
                        grouped = df.groupby(cat_col)[num_col].sum()
                        ax.pie(grouped, labels=grouped.index, autopct="%1.1f%%")
                        ax.axis("equal")
                        st.pyplot(fig)
                else:
                    st.warning("⚠️ No categorical columns found for Pie Chart.")

            elif chart_type == "Scatter Plot":
                num_col = st.selectbox("Select X-axis numeric column", numeric_cols)
                num_col2 = st.selectbox("Select Y-axis numeric column", numeric_cols)
                if num_col and num_col2:
                    sns.scatterplot(x=df[num_col], y=df[num_col2], ax=ax)
                    st.pyplot(fig)

            # Chart download
            img_buf = BytesIO()
            fig.savefig(img_buf, format="png")
            st.download_button("Download Chart as PNG", img_buf.getvalue(), file_name="chart.png", mime="image/png")

    # --- Insights Tab ---
    with tabs[2]:
        st.subheader("💡 Automatic Insights")

        if "Product" in df.columns and "Sales" in df.columns:
            top_product = df.groupby("Product")["Sales"].sum().idxmax()
            st.write(f"✅ **Top Product by Total Sales:** {top_product}")

        if "Region" in df.columns and "Sales" in df.columns:
            top_region = df.groupby("Region")["Sales"].sum().idxmax()
            st.write(f"✅ **Region with Highest Sales:** {top_region}")

        if "Product" in df.columns and "Profit" in df.columns:
            top_profit_product = df.groupby("Product")["Profit"].mean().idxmax()
            st.write(f"✅ **Product with Highest Avg Profit:** {top_profit_product}")

        st.info("Insights are auto-calculated from your uploaded data.")

    # --- Report Tab ---
    with tabs[3]:
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
else:
    st.info("👈 Please upload a CSV or Excel file from the sidebar to get started.")

# Footer
st.markdown("""
    <hr>
    <center>
    <span style="font-size:13px">Made with ❤️ by Sagar • GitHub: <a href="https://github.com/sagar5282" target="_blank">sagar5282</a></span>
    </center>
""", unsafe_allow_html=True)
