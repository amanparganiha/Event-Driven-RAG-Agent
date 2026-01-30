from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


class QdrantStorage:
    def __init__(self, url="http://localhost:6333", collection="docs", dim=3072):
        self.client = QdrantClient(url=url, timeout=30)
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