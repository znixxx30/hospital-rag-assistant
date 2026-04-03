import streamlit as st
import requests

from app.rag import generate_answer

st.set_page_config(page_title="Hospital RAG Assistant")

st.title("🏥 Hospital AI Assistant")

# ------------------ FILE UPLOAD ------------------
st.subheader("📄 Upload Hospital Document")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    if st.button("Upload Document"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )

        if response.status_code == 200:
            st.success("Document uploaded and processed!")
        else:
            st.error("Upload failed")

# ------------------ CHAT HISTORY ------------------
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("💬 Ask Questions")

question = st.text_input("Enter your question:")

if st.button("Ask"):
    if question:
        with st.spinner("Thinking..."):
            answer, _ = generate_answer(question, st.session_state.history)

        # Save history
        st.session_state.history.append(f"Q: {question}")
        st.session_state.history.append(f"A: {answer}")

# ------------------ DISPLAY CHAT ------------------
st.subheader("💬 Chat History")

for item in st.session_state.history:
    if item.startswith("Q:"):
        st.markdown(f"**🧑 {item}**")
    else:
        st.markdown(f"**🤖 {item}**")