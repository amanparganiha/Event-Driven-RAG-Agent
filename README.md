# **🚀 Event-Driven RAG Agent**

> A fully orchestrated, scalable RAG system built for real-world document Q&A — powered by event-driven workflows, semantic search, and an interactive chat interface.
> 

---

## **🎯 Why This Project Matters**

In today's data-driven world, extracting insights from documents efficiently is crucial. This project isn’t just another RAG implementation — it’s a **production-ready, event-driven system** designed for scalability, fault tolerance, and seamless user experience. By combining modern orchestration (Inngest), vector search (Qdrant), and LLMs (OpenAI), it demonstrates how to build resilient AI applications that handle real-world PDF ingestion and intelligent Q&A at scale.

---

## **✨ Key Highlights**

- ✅ **Event-Driven Architecture**: Asynchronous PDF processing using Inngest for durable, retryable workflows.
- ✅ **Scalable Vector Search**: Qdrant-powered semantic search with high-performance embeddings (`text-embedding-3-large`).
- ✅ **Resilient & Observable**: Built-in failure recovery, state tracking, and real-time workflow monitoring.
- ✅ **End-to-End Pipeline**: From PDF upload to intelligent answering — fully automated and modular.
- ✅ **Clean UI/UX**: Streamlit frontend for intuitive document upload and chat-based interaction.

---

## **🛠 Tech Stack & Architecture**

| **Component** | **Technology** | **Why It Was Chosen** |
| --- | --- | --- |
| **Orchestration** | Inngest | Durable workflows, stepwise retries, and event-driven scalability. |
| **Vector DB** | Qdrant | Fast, scalable similarity search with native Docker support. |
| **LLM & Embeddings** | OpenAI (`gpt-4o-mini`, `text-embedding-3-large`) | High-quality embeddings and cost-effective reasoning. |
| **Backend API** | FastAPI | Async-ready, high-performance API framework. |
| **Frontend** | Streamlit | Rapid prototyping with interactive data apps. |
| **Package Manager** | uv | Fast, modern dependency management with virtual envs. |

---

## **📁 Project Structure**

bash

```
.
├── main.py              # FastAPI app + Inngest function definitions
├── streamlit_app.py     # Frontend UI for upload & chat
├── data_loader.py       # PDF parsing & embedding generation
├── vector_db.py         # Qdrant client wrapper (CRUD operations)
├── custom_types.py      # Pydantic models for type safety
├── pyproject.toml       # Project dependencies (uv)
└── .env.example         # Environment template
```

---

## **🚀 Getting Started in <5 Minutes**

### **Prerequisites**

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (fast Python package installer)
- Docker Desktop (for Qdrant)
- Node.js & npm (for Inngest CLI)

### **Quick Start**

1. **Clone & setup**

bash

```
git clone https://github.com/amanparganiha/Event-Driven-RAG-Agent.git
cd Event-Driven-RAG-Agent
cp .env.example .env  # Add your OpenAI key
uv sync
```

1. **Run all services with one command (using a process manager like `tmux` or `concurrently`)**
    
    Or manually in four terminals:
    

bash

```
# Terminal 1: Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Terminal 2: Start FastAPI backend
uv run uvicorn main:app --reload

# Terminal 3: Start Inngest Dev Server
npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest --no-discovery

# Terminal 4: Start Streamlit UI
uv run streamlit run streamlit_app.py
```

---

## **🧠 How It Works (Step-by-Step)**

1. **Upload PDF** via Streamlit UI
2. **Event Triggered** → `rag/ingest_pdf` sent to Inngest
3. **Async Processing**:
    - PDF parsed & chunked (LlamaIndex)
    - Embeddings generated (OpenAI)
    - Vectors stored in Qdrant
4. **User Query**:
    - Semantic search retrieves relevant chunks
    - Context passed to LLM for grounded generation
5. **Response Streamed** back to UI

---

## **🧪 Sample Use Case**

Imagine you upload a **50-page technical whitepaper**. Within minutes:

- The system processes it in the background (no UI blocking)
- You can ask:
    - *“What are the key findings in section 4?”*
    - *“Summarize the proposed architecture.”*
    - *“Compare the methods discussed in pages 20–30.”*

The agent retrieves precise snippets and generates concise, citation-backed answers.

---

## **📈 System Design & Scalability Considerations**

- **Decoupled Workflows**: Each step (parse, embed, store) is independently retryable.
- **Observability**: Inngest dashboard provides real-time function execution logs.
- **Extensible**: Easy to swap LLM providers, vector DBs, or chunking strategies.
- **Container Ready**: Qdrant runs in Docker; entire system can be containerized.

---

## **🔮 Future Enhancements (Roadmap)**

- Multi-format support (DOCX, PPT, HTML)
- Hybrid search (keyword + semantic)
- User authentication & document scoping
- Advanced RAG techniques (re-ranking, HyDE)
- Cloud deployment (AWS/GCP) with Terraform

---

## **🤔 FAQ**

**Q: Why Inngest over Celery or Airflow?**

A: Inngest provides built-in durability, state management, and a visual debugger — ideal for event-driven, multi-step AI workflows.

**Q: Can this handle 10,000 PDFs?**

A: Yes — Qdrant scales horizontally, and Inngest queues manage ingestion throughput. Embedding generation can be batched/parallelized.

**Q: Is this usable in production today?**

A: The architecture is production-ready. Adding monitoring, auth, and deployment configs would make it fully productionizable.

---

## **👨‍💻 Contributing**

Contributions are welcome! Please open an issue or submit a PR for:

- New features
- Bug fixes
- Documentation improvements
- Performance optimizations

---

## **📬 Contact & Links**

- **GitHub**: [amanparganiha/Event-Driven-RAG-Agent](https://github.com/amanparganiha/Event-Driven-RAG-Agent)

---
