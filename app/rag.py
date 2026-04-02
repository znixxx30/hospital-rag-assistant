from groq import Groq
import os
from dotenv import load_dotenv

from app.query import retrieve_chunks

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question: str):
    # Step 1: Retrieve chunks
    chunks = retrieve_chunks(question)

    # Step 2: Build context
    context = "\n\n".join([c["content"] for c in chunks])

    # Step 3: Prompt
    prompt = f"""
You are a hospital assistant.

Answer the question clearly and completely using ONLY the context.
If answer is not present, say:
"I don't have that information in the provided document."

Context:
{context}

Question:
{question}
"""

    # Step 4: Call LLM
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # store answer first
    answer = response.choices[0].message.content

    # return BOTH
    return answer, chunks