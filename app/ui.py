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

with st.form(key="chat_form", clear_on_submit=True):
    question = st.text_input("Enter your question:")
    submit = st.form_submit_button("Ask")

if submit and question:
    with st.spinner("Thinking..."):
        answer, chunks = generate_answer(question, st.session_state.history)

    # Extract sources
    sources = [f"page {c['metadata']['page']}" for c in chunks]
    sources = list(set(sources))

    # Save history
    st.session_state.history.append(f"Q: {question}")
    st.session_state.history.append(
        f"A: {answer} (Sources: {', '.join(sources)})"
    )
# ------------------ DISPLAY CHAT ------------------
st.subheader("💬 Chat History")

for item in st.session_state.history:
    if item.startswith("Q:"):
        st.markdown(f"**🧑 {item}**")
    else:
        st.markdown(f"**🤖 {item}**")