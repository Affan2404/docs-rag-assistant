import os, time
from dotenv import load_dotenv
from anthropic import Anthropic
from retrieve import retrieve
from config import CLAUDE_MODEL, MAX_TOKENS, TOP_K
from logger import logger

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a support assistant answering questions using only the
provided context from Freshdesk help articles. Rules:
- Answer only using the given context. Do not use outside knowledge.
- If the context doesn't contain the answer, say so clearly instead of guessing.
- Always mention which source file(s) your answer is based on.
- Keep answers concise and direct."""

NO_CONTEXT_MESSAGE = (
    "I don't have information about that in the Freshdesk documentation "
    "I have access to. Try rephrasing, or ask about knowledge base management, "
    "multilingual support, or automation rules."
)

def build_context(chunks):
    parts = []
    for c in chunks:
        parts.append(f"[Source: {c['source_file']}]\n{c['text']}")
    return "\n\n---\n\n".join(parts)

def answer_question(query, top_k=TOP_K):
    start_time = time.time()
    chunks = retrieve(query, top_k=top_k)

    if not chunks:
        elapsed = time.time() - start_time
        logger.info(f"query='{query}' | chunks_found=0 | tokens=0 | latency={elapsed:.2f}s | grounded=False")
        return NO_CONTEXT_MESSAGE, chunks

    context = build_context(chunks)
    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )

    elapsed = time.time() - start_time
    total_tokens = response.usage.input_tokens + response.usage.output_tokens
    logger.info(f"query='{query}' | chunks_found={len(chunks)} | tokens={total_tokens} | latency={elapsed:.2f}s | grounded=True")

    return response.content[0].text, chunks

if __name__ == "__main__":
    while True:
        query = input("\nAsk a question (or 'quit'): ")
        if query.lower() == "quit":
            break

        answer, chunks = answer_question(query)
        print(f"\nAnswer:\n{answer}")