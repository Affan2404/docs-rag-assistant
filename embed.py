import json
from sentence_transformers import SentenceTransformer
import chromadb
from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL

CHUNKS_FILE = "data/processed/chunks.json"

model = SentenceTransformer(EMBEDDING_MODEL)

with open(CHUNKS_FILE, encoding="utf-8") as f:
    chunks = json.load(f)

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

texts = [chunk["text"] for chunk in chunks]
ids = [str(chunk["id"]) for chunk in chunks]
metadatas = [{"source_file": chunk["source_file"]} for chunk in chunks]

print(f"Embedding {len(texts)} chunks...")
embeddings = model.encode(texts).tolist()

collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=texts,
    metadatas=metadatas
)

print(f"Stored {collection.count()} chunks in ChromaDB at ./{CHROMA_DIR}")