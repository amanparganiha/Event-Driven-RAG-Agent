import os

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


# A single shared client per process. For the embedded in-memory mode this is
# essential: each QdrantClient(":memory:") owns its own isolated storage, so we
# must reuse one instance for the whole app (it also survives Streamlit reruns
# because imported modules are cached in sys.modules).
_client = None


def get_client() -> QdrantClient:
    global _client
    if _client is not None:
        return _client

    url = os.getenv("QDRANT_URL")
    if url:
        # Remote / hosted Qdrant (e.g. local Docker or Qdrant Cloud).
        _client = QdrantClient(
            url=url,
            api_key=os.getenv("QDRANT_API_KEY") or None,
            timeout=30,
        )
    else:
        # Embedded in-memory Qdrant. No external service required, which is what
        # lets the app run on Streamlit Community Cloud. Data is lost when the
        # process restarts; set QDRANT_URL to switch to a persistent backend.
        _client = QdrantClient(location=":memory:")

    return _client


class QdrantStorage:
    def __init__(self, collection="docs", dim=3072):
        self.client = get_client()
        self.collection = collection

        if not self.client.collection_exists(collection_name=self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=dim,
                    distance=Distance.COSINE,
                ),
            )

    def upsert(self, ids, vectors, payloads):
        points = [
            PointStruct(
                id=ids[i],
                vector=vectors[i],
                payload=payloads[i],
            )
            for i in range(len(ids))
        ]

        self.client.upsert(
            collection_name=self.collection,
            points=points,
        )

    def search(self, query_vector, top_k=5):
        results = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            with_payload=True,
            limit=top_k,
        )

        contexts = []
        sources = set()

        if hasattr(results, 'points'):
            points = results.points
        else:
            points = results

        for point in points:

            if hasattr(point, 'payload'):
                payload = point.payload
            elif isinstance(point, dict) and 'payload' in point:
                payload = point['payload']
            else:
                continue

            if not payload:
                continue

            text = payload.get("text")
            source = payload.get("source")

            if text:
                contexts.append(text)
            if source:
                sources.add(source)

        return {
            "contexts": contexts,
            "sources": list(sources),
        }
