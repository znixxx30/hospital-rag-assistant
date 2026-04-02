from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from app.db import supabase

def load_split_embed_store(file_path: str):
    # Load PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    print(f"Total chunks: {len(chunks)}")

    # Embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [chunk.page_content for chunk in chunks]
    vectors = model.encode(texts)

    # Insert into Supabase
    for i, chunk in enumerate(chunks):
        data = {
            "content": chunk.page_content,
            "embedding": vectors[i].tolist(),  # IMPORTANT
            "metadata": {"page": chunk.metadata.get("page", 0)}
        }

        supabase.table("documents").insert(data).execute()

    print("✅ Data inserted into Supabase")


if __name__ == "__main__":
    load_split_embed_store("data/ai_ml_doc_assignement.pdf")