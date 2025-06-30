import streamlit as st
import openai

st.title("🧠 Insights - Ask AI")

if "df" not in st.session_state:
    st.warning("Please upload data from the Home page first.")
else:
    df = st.session_state["df"]
    st.write(df.head())

    question = st.text_input("Ask a question about the data")
    if question:
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        sample = df.head(10).to_string()
        prompt = f"Dataset:\n{sample}\n\nQuestion: {question}"
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response['choices'][0]['message']['content']
        st.markdown("### 🤖 Answer")
        st.write(answer)
        st.session_state["ai_answer"] = answer
        st.session_state["ai_question"] = question
