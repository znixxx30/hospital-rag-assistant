from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    print(f"Total pages loaded: {len(documents)}")
    
    for i, doc in enumerate(documents):
        print(f"\n--- Page {i+1} ---")
        print(doc.page_content[:300])  # preview first 300 chars
    
    return documents


if __name__ == "__main__":
    docs = load_pdf("data/ai_ml_doc_assignement.pdf")