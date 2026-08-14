import os, re, json
from config import MAX_CHARS, OVERLAP_SENTENCES

RAW_DIR = "data/raw"
OUTPUT_FILE = "data/processed/chunks.json"

def split_into_sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

def chunk_sentences(sentences):
    chunks, current = [], []
    current_len = 0

    for sentence in sentences:
        if current_len + len(sentence) > MAX_CHARS and current:
            chunks.append(" ".join(current))
            current = current[-OVERLAP_SENTENCES:]
            current_len = sum(len(s) for s in current)
        current.append(sentence)
        current_len += len(sentence)

    if current:
        chunks.append(" ".join(current))
    return chunks

def process_all_files():
    all_chunks = []
    chunk_id = 0

    for filename in os.listdir(RAW_DIR):
        if not filename.endswith(".txt"):
            continue

        with open(os.path.join(RAW_DIR, filename), encoding="utf-8") as f:
            text = f.read()

        sentences = split_into_sentences(text)
        pieces = chunk_sentences(sentences)

        for piece in pieces:
            all_chunks.append({
                "id": chunk_id,
                "source_file": filename,
                "text": piece
            })
            chunk_id += 1

        print(f"{filename}: {len(pieces)} chunk(s)")

    return all_chunks

def main():
    os.makedirs("data/processed", exist_ok=True)
    chunks = process_all_files()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"\nTotal: {len(chunks)} chunks saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()