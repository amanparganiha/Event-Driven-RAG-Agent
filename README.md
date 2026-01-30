# RAGProductionApp

Simple Retrieval-Augmented Generation (RAG) demo using PDF ingestion, embeddings, a vector DB (Qdrant), and an LLM via OpenAI. Includes a Streamlit UI to upload PDFs and ask questions, an Inngest workflow for ingestion and query orchestration, and a FastAPI app that exposes Inngest functions.

## Features
- PDF load + chunking (llama_index PDFReader + SentenceSplitter)
- Embedding via OpenAI embeddings
- Vector storage/search with Qdrant
- Orchestrated ingestion and query flows using Inngest
- Streamlit UI for upload + Q&A
- FastAPI app to serve Inngest functions

## Repo layout
- data_loader.py — PDF loading, chunking, embeddings
- vector_db.py — Qdrant client wrapper
- main.py — Inngest functions (ingest + query) and FastAPI app
- streamlit_app.py — Streamlit frontend for upload and queries
- custom_types.py — Pydantic models used by workflows

## Requirements
- Python 3.10+
- Qdrant (local or remote)
- OpenAI API key
- Inngest local dev server (for dev workflow / observability)
- Recommended pip packages (example):
    - fastapi
    - uvicorn[standard]
    - streamlit
    - python-dotenv
    - openai (or openai-compatible client used in code)
    - qdrant-client
    - llama-index
    - inngest
    - pydantic

Create a virtualenv and install:
pip install fastapi uvicorn streamlit python-dotenv qdrant-client llama-index inngest pydantic

## Environment variables
Create a `.env` file with at least:
OPENAI_API_KEY=sk-...
Optionally:
INNGEST_API_BASE=http://127.0.0.1:8288/v1
QDRANT_URL=http://localhost:6333

## Run (local development)
1. Start Qdrant
     - Quick (Docker): docker run -p 6333:6333 qdrant/qdrant
     - Or use your hosted Qdrant and set QDRANT_URL

2. Start Inngest local dev server (used by the Streamlit UI to send events)
     - Run your local Inngest dev server per Inngest docs (e.g., `inngest dev` or equivalent).

3. Run the FastAPI app (Inngest functions)
     uvicorn main:app --reload --port 8000

4. Run the Streamlit UI
     streamlit run streamlit_app.py

5. Use the UI
     - Upload a PDF to trigger ingestion (chunks → embeddings → upsert to Qdrant)
     - Ask a question in the form to query, retrieve contexts, and get an LLM answer

## Notes & tips
- Chunk sizing is controlled in data_loader.py (SentenceSplitter).
- Embedding model and dims are defined in data_loader.py (adjust to fit your account/features).
- Qdrant collection is created automatically by QdrantStorage if missing.
- In production, secure API keys and configure Inngest and Qdrant appropriately.

## Troubleshooting
- If no search results, verify:
    - Qdrant is reachable at the expected URL
    - Embeddings completed successfully during ingestion
    - OPENAI_API_KEY is set and valid
- Inspect Inngest runs via the local Inngest dashboard / API to see step outputs and errors.

## License
Project skeleton — adapt and extend for your use.
