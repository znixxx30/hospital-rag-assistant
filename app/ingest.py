from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

def load_split_embed(file_path: str):
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

    # Load free embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Convert chunks → embeddings
    texts = [chunk.page_content for chunk in chunks]
    vectors = model.encode(texts)

    # Preview
    for i in range(2):
        print(f"\n--- Sample Embedding {i+1} ---")
        print(vectors[i][:10])

    return chunks, vectors


if __name__ == "__main__":
    chunks, vectors = load_split_embed("data/ai_ml_doc_assignement.pdf")
