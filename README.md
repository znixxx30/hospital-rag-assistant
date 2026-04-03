# 🏥 Hospital RAG Assistant

An AI-powered Patient Query Assistant built using Retrieval-Augmented Generation (RAG).
The system answers user queries strictly based on a provided hospital document.

---

## 🚀 Features

* 📄 PDF Upload & Ingestion
* ✂️ Smart Text Chunking
* 🧠 Semantic Search using Embeddings
* 🗄️ Vector Database (Supabase pgvector)
* 🤖 LLM-powered Answers (Groq - Llama 3.1)
* 🔍 Source Attribution (Page Numbers)
* 💬 Chat History (Conversational AI)
* 🖥️ Streamlit UI for interaction

---

## 🧠 Architecture

```
User (UI / API)
      ↓
FastAPI Backend
      ↓
PDF Upload → Text Extraction → Chunking
      ↓
Embeddings (SentenceTransformers)
      ↓
Supabase (pgvector)
      ↓
Query → Embedding → Similarity Search
      ↓
Top-K Chunks
      ↓
LLM (Groq - Llama 3.1)
      ↓
Final Answer + Sources
```

---

## 🛠️ Tech Stack

* FastAPI
* Streamlit
* SentenceTransformers (all-MiniLM-L6-v2)
* Supabase (PostgreSQL + pgvector)
* Groq API (Llama 3.1)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/hospital-rag-assistant.git
cd hospital-rag-assistant
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

Or manually:

```
pip install fastapi uvicorn streamlit sentence-transformers supabase groq python-dotenv python-multipart requests
```

---

### 3️⃣ Setup Environment Variables

Create `.env` file:

```
SUPABASE_URL=your_url
SUPABASE_KEY=your_secret_key
GROQ_API_KEY=your_groq_key
```

---

### 4️⃣ Run Backend

```
uvicorn app.main:app --reload
```

---

### 5️⃣ Run UI

```
python -m streamlit run app/ui.py
```

---

## 📌 API Endpoints

### 📄 Upload Document

```
POST /upload
```

### 💬 Ask Question

```
POST /query
```

Request:

```json
{
  "question": "What is ICU cost?"
}
```

Response:

```json
{
  "answer": "ICU cost is $600 per day.",
  "sources": ["page 5"]
}
```

---

## 🧪 Sample Queries

* What are OPD timings?
* Who is the cardiologist?
* What is the cost of MRI?
* What is ICU cost per day?
* What is the emergency number?

---

## 🚫 Important Constraint

The system answers **ONLY from the document**.
If information is not found:

```
"I don't have that information in the provided document."
```

---

## 🎯 Key Highlights

* Prevents hallucination using RAG
* Supports conversational queries (chat history)
* Handles real-world document QA scenarios


---

## 👨‍💻 Author

Anshuman Singh