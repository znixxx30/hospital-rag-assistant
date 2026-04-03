from groq import Groq
import os
from dotenv import load_dotenv

from app.query import retrieve_chunks

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question: str, history=None):
    if history is None:
        history = []

    # Step 1: Retrieve chunks
    chunks = retrieve_chunks(question)

    # Step 2: Build context
    context = "\n\n".join([c["content"] for c in chunks])

    # Step 3: Build history string
    history_text = "\n".join(history)

    prompt = f"""
You are a hospital assistant.

Answer using ONLY the provided context.
Be careful about slight variations in wording.

If answer is not present, say:
"I don't have that information in the provided document."

Previous Conversation:
{history_text}

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return answer, chunks