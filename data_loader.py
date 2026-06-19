from openai import OpenAI
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = "text-embedding-3-large"
EMBED_DIM = 3072

splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)

# Lazily-created default client. Built only when needed so importing this module
# does not require OPENAI_API_KEY to be set (the deployed app passes a per-user
# client instead).
_default_client = None


def _get_default_client() -> OpenAI:
    global _default_client
    if _default_client is None:
        _default_client = OpenAI()
    return _default_client


def load_and_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path)
    texts = [d.text for d in docs if getattr(d, "text", None)]
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks


def embed_texts(texts: list[str], client: OpenAI | None = None) -> list[list[float]]:
    client = client or _get_default_client()
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]