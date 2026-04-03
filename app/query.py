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

    # Step 3: Safety check
    if not response.data:
        return []

    return response.data

