"""
Self-contained Streamlit RAG app — the deployment entrypoint for Streamlit Cloud.

This is a single-process version of the event-driven system. It runs the same
RAG pipeline (chunk -> embed -> store -> search -> answer) synchronously, with no
Inngest, FastAPI, or Docker, so it can run anywhere a single Streamlit app runs.

The original event-driven stack (main.py + streamlit_app.py) is kept for local
runs and demos of the Inngest/FastAPI architecture.
"""

import os
import tempfile
import uuid

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from data_loader import load_and_chunk_pdf, embed_texts
from vector_db import QdrantStorage

load_dotenv()

st.set_page_config(page_title="RAG PDF Q&A", page_icon="📄", layout="centered")

CHAT_MODEL = "gpt-4o-mini"


def get_api_key() -> str:
    """Read the OpenAI key from the sidebar (per user), falling back to env/secrets."""
    with st.sidebar:
        st.header("🔑 OpenAI API Key")
        st.caption(
            "Paste your own key — it's used only for your session, never stored "
            "or charged to anyone else."
        )
        key = st.text_input(
            "OpenAI API key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            placeholder="sk-...",
            label_visibility="collapsed",
        )
        st.markdown(
            "[Get a key →](https://platform.openai.com/api-keys)",
            help="You need an OpenAI account with billing enabled.",
        )
    return key.strip()


@st.cache_resource
def get_store() -> QdrantStorage:
    return QdrantStorage()


@st.cache_resource(show_spinner=False)
def get_openai(api_key: str) -> OpenAI:
    # Cached per distinct key so each user reuses their own client.
    return OpenAI(api_key=api_key)


def ingest_pdf(uploaded_file, client: OpenAI) -> int:
    """Save the upload to a temp file, chunk, embed, and store. Returns #chunks."""
    # Write to a temp file because the PDF reader works off a filesystem path.
    # On Windows the file must be closed before it can be re-opened by the reader.
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        tmp.write(uploaded_file.getbuffer())
        tmp.close()
        chunks = load_and_chunk_pdf(tmp.name)
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass

    if not chunks:
        return 0

    vecs = embed_texts(chunks, client=client)
    source_id = uploaded_file.name
    ids = [
        str(uuid.uuid5(uuid.NAMESPACE_URL, name=f"{source_id}:{i}"))
        for i in range(len(chunks))
    ]
    payloads = [{"source": source_id, "text": chunks[i]} for i in range(len(chunks))]
    get_store().upsert(ids, vecs, payloads)
    return len(chunks)


def answer_question(question: str, client: OpenAI, top_k: int = 5):
    query_vec = embed_texts([question], client=client)[0]
    found = get_store().search(query_vec, top_k)

    context_block = "\n\n".join(f"- {c}" for c in found["contexts"])
    user_content = (
        "Use the following context to answer the question:\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n"
        "Answer concisely using the context above."
    )

    res = client.chat.completions.create(
        model=CHAT_MODEL,
        max_tokens=1024,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You answer questions using only the provided context.",
            },
            {"role": "user", "content": user_content},
        ],
    )
    answer = (res.choices[0].message.content or "").strip()
    return answer, found["sources"], len(found["contexts"])


api_key = get_api_key()

if "ingested_files" not in st.session_state:
    st.session_state.ingested_files = []

st.title("📄 RAG PDF Q&A")
st.caption("Upload PDFs, then ask questions grounded in their contents.")

if not api_key:
    st.info("👈 Enter your OpenAI API key in the sidebar to get started.")
    st.stop()

client = get_openai(api_key)

st.subheader("1. Upload a PDF")
uploaded = st.file_uploader("Choose a PDF", type=["pdf"], accept_multiple_files=False)

if uploaded is not None:
    if st.button(f"Ingest “{uploaded.name}”", type="primary"):
        with st.spinner("Parsing, embedding, and indexing…"):
            n = ingest_pdf(uploaded, client)
        if n:
            st.session_state.ingested_files.append(uploaded.name)
            st.success(f"Ingested {n} chunks from {uploaded.name}.")
        else:
            st.warning("No extractable text found in that PDF.")

if st.session_state.ingested_files:
    st.caption("Indexed documents: " + ", ".join(st.session_state.ingested_files))

st.divider()

st.subheader("2. Ask a question")
with st.form("rag_query_form"):
    question = st.text_input("Your question")
    top_k = st.number_input(
        "Chunks to retrieve", min_value=1, max_value=20, value=5, step=1
    )
    submitted = st.form_submit_button("Ask")

if submitted and question.strip():
    with st.spinner("Searching and generating an answer…"):
        answer, sources, num_contexts = answer_question(
            question.strip(), client, int(top_k)
        )

    st.subheader("Answer")
    st.write(answer or "(No answer)")
    if sources:
        st.caption("Sources")
        for s in sources:
            st.write(f"- {s}")
    st.caption(f"Retrieved {num_contexts} context chunk(s).")
elif submitted:
    st.warning("Please enter a question.")
