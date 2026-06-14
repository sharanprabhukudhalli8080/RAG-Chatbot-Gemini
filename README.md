# 🤖 RAG-Chatbot-Gemini

AI-powered PDF Question Answering System built using **Gemini 2.5 Flash**, **LangChain**, **ChromaDB**, and **Streamlit**.

Upload one or more PDF documents, ask questions in natural language, and receive context-aware answers using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

✅ Multi-PDF Upload

✅ Semantic Search

✅ ChromaDB Vector Database

✅ Gemini 2.5 Flash Integration

✅ Conversational Memory

✅ Source Citations

✅ Chat History

✅ Suggested Questions

✅ Download Chat History

✅ Modern Streamlit Interface

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini 2.5 Flash
- LangChain
- ChromaDB
- HuggingFace Embeddings
- PyPDF
- Retrieval-Augmented Generation (RAG)

---

## 📂 Project Structure

```text
RAG-Chatbot-Gemini/
│
├── app.py
│
├── utils/
│   ├── pdf_loader.py
│   ├── vector_store.py
│   ├── llm_handler.py
│   └── pdf_export.py
│
├── chroma_db/
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/sharanprabhukudhalli8080/RAG-Chatbot-Gemini.git

cd RAG-Chatbot-Gemini
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Get API Key from:

https://aistudio.google.com/

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will open at:

```text
http://localhost:8501
```

---

## 📸 Workflow

1. Upload PDF documents
2. PDFs are split into chunks
3. Chunks are embedded using HuggingFace embeddings
4. ChromaDB stores vector embeddings
5. User asks a question
6. Relevant chunks are retrieved
7. Gemini generates context-aware answers
8. Sources are displayed

---

## 🧠 Architecture

```text
PDF Files
    │
    ▼
PDF Loader
    │
    ▼
Text Chunking
    │
    ▼
Embeddings
    │
    ▼
ChromaDB
    │
    ▼
Retriever
    │
    ▼
Gemini 2.5 Flash
    │
    ▼
Answer + Sources
```

---

## 📚 Example Questions

- Summarize this document
- What are the key takeaways?
- Explain the main topics
- What conclusions are mentioned?
- What does page 5 discuss?

---

## 🎯 Future Improvements

- Hybrid Search (BM25 + ChromaDB)
- Streaming Responses
- PDF Export
- Authentication System
- DOCX/TXT/PPTX Support
- Voice Assistant
- Docker Deployment
- AWS Deployment

---

## 👨‍💻 Author

Sharanprabhu Kudhalli

Computer Science Engineering Student

Interested in Data Science, Machine Learning, Generative AI, and Data Analytics.

---

## 📄 License

MIT License

---

⭐ If you found this project useful, please give it a star.
