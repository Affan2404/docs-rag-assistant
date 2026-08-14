import json, os, hashlib

def _hash_text(text):
    return hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()

def load_json_cache(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json_cache(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)