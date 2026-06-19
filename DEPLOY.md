# Deploying to Streamlit Community Cloud

The deployed app is **`app.py`** — a single-process version of this project that
runs the full RAG pipeline (chunk → embed → store → search → answer)
synchronously. It does **not** use Inngest, FastAPI, or Docker, because Streamlit
Cloud only runs one Streamlit process.

> The original event-driven stack (`main.py` + `streamlit_app.py`) is kept for
> local runs that showcase the Inngest/FastAPI architecture. See the README.

## Vector store

By default the app uses an **embedded in-memory Qdrant** — no external service
needed. Uploaded PDFs are indexed in memory and are **lost when Streamlit Cloud
restarts the app** (e.g. after inactivity); just re-upload. To make storage
persistent, set `QDRANT_URL` (+ `QDRANT_API_KEY`) to a Qdrant Cloud cluster — no
code change required.

## Steps

1. **Push to GitHub.** Make sure `app.py`, `requirements.txt`, `data_loader.py`,
   `vector_db.py`, and `custom_types.py` are committed. Do **not** commit `.env`
   or `.streamlit/secrets.toml`.

2. **Create the app** at https://share.streamlit.io → *New app* → pick your repo
   and branch.
   - **Main file path:** `app.py`
   - (Advanced settings) **Python version:** 3.13

3. **Secrets (optional).** You do **not** need to set `OPENAI_API_KEY` — each
   visitor pastes their own key in the app's sidebar, so usage is billed to them,
   not to you. Only add secrets if you want a persistent vector store:
   ```toml
   QDRANT_URL = "https://your-cluster.cloud.qdrant.io:6333"
   QDRANT_API_KEY = "your-qdrant-api-key"
   ```

4. **Deploy.** First boot installs dependencies (a few minutes — LlamaIndex is
   sizeable). Once up, paste an OpenAI key in the sidebar, upload a PDF, click
   *Ingest*, then ask a question.

## Run locally first (recommended)

```bash
uv sync                 # or: pip install -r requirements.txt
cp .env.example .env    # add your OPENAI_API_KEY
uv run streamlit run app.py
```

## Notes / limits

- Streamlit Cloud free tier has ~1 GB RAM. Very large PDFs or many concurrent
  uploads can hit that limit; in-memory vectors also count against it.
- Embedding model is `text-embedding-3-large` (3072-dim) and the chat model is
  `gpt-4o-mini` — both call the OpenAI API, which is billed to your key.
- `requirements.txt` (not `pyproject.toml`) drives the Cloud build, so the
  Inngest/FastAPI deps are excluded from the deployed image.
