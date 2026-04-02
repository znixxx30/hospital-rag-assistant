from sentence_transformers import SentenceTransformer
from app.db import supabase

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(query: str, top_k: int = 5):
    # Step 1: Convert query → embedding
    query_vector = model.encode(query).tolist()

    # Step 2: Call Supabase RPC function
    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_vector,
            "match_count": top_k
        }
    ).execute()

    return response.data


if __name__ == "__main__":
    question = "What is ICU cost?"
    results = retrieve_chunks(question)

    print("\n🔍 Top Results:\n")

    for r in results:
        print("Content:", r["content"][:200])
        print("Metadata:", r["metadata"])
        print("Similarity:", r["similarity"])
        print("-" * 50)