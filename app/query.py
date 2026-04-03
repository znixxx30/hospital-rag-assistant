from sentence_transformers import SentenceTransformer
from app.db import supabase

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(query: str, top_k: int = 8):
    # Normalize query (VERY IMPORTANT)
    clean_query = query.lower().strip()

    #  Add small query expansion (improves retrieval)
    expanded_query = f"{clean_query} hospital information details"

    #  Convert to embedding
    query_vector = model.encode(expanded_query).tolist()

    #  Call Supabase RPC
    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_vector,
            "match_count": top_k
        }
    ).execute()

    #  Safety check
    if not response.data:
        return []

    #  Sort by similarity (extra safety)
    results = sorted(response.data, key=lambda x: x["similarity"], reverse=True)

    return results