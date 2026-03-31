import uuid
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient, models
from src.schemas.chunk import Chunk
from dotenv import load_dotenv

load_dotenv() 

embedding_model = OpenAIEmbeddings(
    model="openai/text-embedding-3-large",
    base_url="https://openrouter.ai/api/v1"
)

qdrant_client = QdrantClient(url="http://localhost:6333")


def embed_and_store_chunks(chunks: list[Chunk], collection_name: str = "customer_chunks", batch_size:int = 10):
    """
    Embed the chunks using the specified embedding model and store them in the Qdrant collection.
    """
    print(f"Initializing Qdrant collection: {collection_name}...")

    if qdrant_client.collection_exists(collection_name):
        qdrant_client.delete_collection(collection_name)

    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=3072, distance=models.Distance.COSINE)
    )

    all_vectors: list[list[float]] = []

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start+batch_size]

        text_to_embed = [chunk.content for chunk in batch]

        vectors = embedding_model.embed_documents(text_to_embed)

        all_vectors.extend(vectors)

    print(f"Generated embeddings for {len(chunks)} chunks. Storing in Qdrant...")
    
    points: list[models.PointStruct] = []

    for chunk, vector in zip(chunks, all_vectors):
        payload_data = {
            'source_document': chunk.source_document,
            'content': chunk.content,
            **chunk.metadata
        }

        point = models.PointStruct(
            id=uuid.uuid4(),
            vector=vector,
            payload=payload_data
        )

        points.append(point)

    qdrant_client.upsert(
        collection_name=collection_name,
        points=points
    )

    print(f"Stored {len(points)} points in Qdrant collection '{collection_name}'.")


if __name__ == "__main__":
    from src.rag.chunking import split_text_into_chunks
    from src.rag.ingest import load_documents_from_directory

    directory_path = "/Users/bachng/Coding/Multi-Agent-Customer-Support-System/docs"  # Update this path to your documents directory
    documents = load_documents_from_directory(directory_path)
    chunks = split_text_into_chunks(documents)
    embed_and_store_chunks(chunks)