from .embedding import create_embedding
from .vector_store import client, COLLECTION_NAME

def search_documents(
    question: str,
    limit: int = 200
):
    """
    Convert the question into an embedding
    and search Qdrant for similar document chunks.
    """

    query_vector = create_embedding(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True
    )

    return results.points