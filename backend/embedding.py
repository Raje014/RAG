import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)

model = SentenceTransformer(MODEL_NAME)


def create_embedding(text: str):
    """
    Convert text into a vector embedding.
    """

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()


def create_embeddings(texts: list[str]):
    """
    Convert multiple texts into vector embeddings.
    """

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()


def get_embedding_dimension():
    return model.get_sentence_embedding_dimension()