import os
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import logging
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

from dotenv import load_dotenv

load_dotenv()

def _get_int(key, default):
    val = os.getenv(key)
    return int(val) if val else default

def _get_float(key, default):
    val = os.getenv(key)
    return float(val) if val else default

# Storage
CHROMA_DIR = os.getenv("CHROMA_DIR", "chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "freshdesk_docs")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Chunking
MAX_CHARS = _get_int("MAX_CHARS", 500)
OVERLAP_SENTENCES = _get_int("OVERLAP_SENTENCES", 1)

# Retrieval
TOP_K = _get_int("TOP_K", 3)
MAX_DISTANCE = _get_float("MAX_DISTANCE", 1.0)

# Generation
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = _get_int("MAX_TOKENS", 500)