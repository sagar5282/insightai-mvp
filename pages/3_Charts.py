import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Charts")

if "df" not in st.session_state:
    st.warning("Please upload data from Home page.")
else:
    df = st.session_state["df"]
    numeric_cols = df.select_dtypes(include=['int', 'float']).columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()

    if numeric_cols:
        chart = st.selectbox("Chart type", ["Histogram", "Bar"])
        num_col = st.selectbox("Numeric Column", numeric_cols)

        if chart == "Histogram":
            fig, ax = plt.subplots()
            sns.histplot(df[num_col], kde=True, ax=ax)
            st.pyplot(fig)

        if chart == "Bar" and cat_cols:
            cat_col = st.selectbox("Categorical Column (Group By)", cat_cols)
            fig, ax = plt.subplots()
            sns.barplot(x=cat_col, y=num_col, data=df, ax=ax)
            st.pyplot(fig)
