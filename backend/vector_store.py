import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance


load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION",
    "document_chunks"
)

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)


def get_client():
    return client


def get_collection_name():
    return COLLECTION_NAME

def recreate_collection():

    if client.collection_exists(COLLECTION_NAME):

        client.delete_collection(
            collection_name=COLLECTION_NAME
        )

    client.create_collection(

        collection_name=COLLECTION_NAME,

        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print(
        f"Collection '{COLLECTION_NAME}' created."
    )