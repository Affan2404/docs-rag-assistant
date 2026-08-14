from sentence_transformers import SentenceTransformer
import chromadb
from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K, MAX_DISTANCE

model = SentenceTransformer(EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(name=COLLECTION_NAME)

def retrieve(query, top_k=TOP_K, max_distance=MAX_DISTANCE):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    chunks = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        if distance <= max_distance:
            chunks.append({
                "text": text,
                "source_file": metadata["source_file"],
                "distance": distance
            })
    return chunks

if __name__ == "__main__":
    while True:
        query = input("\nAsk a question (or 'quit'): ")
        if query.lower() == "quit":
            break

        query_embedding = model.encode([query]).tolist()
        results = collection.query(query_embeddings=query_embedding, n_results=TOP_K)

        print(f"\nTop {TOP_K} raw matches (threshold = {MAX_DISTANCE}):\n")
        for i, (text, metadata, distance) in enumerate(zip(
            results["documents"][0], results["metadatas"][0], results["distances"][0]
        ), 1):
            status = "PASS" if distance <= MAX_DISTANCE else "FILTERED OUT"
            print(f"{i}. [{status}] [{metadata['source_file']}] distance: {distance:.4f}")
            print(f"   {text[:120]}...\n")