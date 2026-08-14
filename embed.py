import json
from sentence_transformers import SentenceTransformer
import chromadb
from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL
from cache import _hash_text, load_json_cache, save_json_cache

CHUNKS_FILE = "data/processed/chunks.json"
MANIFEST_FILE = "data/processed/embed_manifest.json"

with open(CHUNKS_FILE, encoding="utf-8") as f:
    chunks_raw_text = f.read()

chunks = json.loads(chunks_raw_text)
current_hash = _hash_text(chunks_raw_text)

manifest = load_json_cache(MANIFEST_FILE)

if manifest.get("chunks_hash") == current_hash:
    print("No changes detected in chunks.json since the last embed run - skipping re-embedding.")
    print(f"(To force a rebuild, delete {MANIFEST_FILE} and re-run this script.)")
else:
    model = SentenceTransformer(EMBEDDING_MODEL)

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

    save_json_cache(MANIFEST_FILE, {"chunks_hash": current_hash})