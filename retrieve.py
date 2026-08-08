from sentence_transformers import SentenceTransformer
import chromadb

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "freshdesk_docs"
TOP_K = 3

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(name=COLLECTION_NAME)

def retrieve(query, top_k=TOP_K):
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
        chunks.append({
            "text": text,
            "source_file": metadata["source_file"],
            "distance": distance
        })
    return chunks

# Quick manual test loop - type a question, see which chunks come back
if __name__ == "__main__":
    while True:
        query = input("\nAsk a question (or 'quit'): ")
        if query.lower() == "quit":
            break

        results = retrieve(query)
        print(f"\nTop {len(results)} matches:\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r['source_file']}] (distance: {r['distance']:.4f})")
            print(f"   {r['text'][:150]}...\n")