import json
from retrieve import retrieve

EVAL_FILE = "data/eval_set.json"

def run_eval():
    with open(EVAL_FILE, encoding="utf-8") as f:
        eval_cases = json.load(f)

    correct = 0
    results = []

    for case in eval_cases:
        question = case["question"]
        expected = case["expected_source"]

        retrieved_chunks = retrieve(question)
        retrieved_sources = [c["source_file"] for c in retrieved_chunks]

        found = expected in retrieved_sources
        if found:
            correct += 1

        results.append({
            "question": question,
            "expected": expected,
            "retrieved_sources": retrieved_sources,
            "found": found
        })

    print("\n--- Retrieval Eval Results ---\n")
    for r in results:
        status = "PASS" if r["found"] else "FAIL"
        print(f"[{status}] {r['question']}")
        print(f"  expected: {r['expected']}")
        print(f"  got:      {r['retrieved_sources']}\n")

    total = len(eval_cases)
    accuracy = (correct / total) * 100 if total else 0
    print(f"Accuracy: {correct}/{total} ({accuracy:.1f}%)")

if __name__ == "__main__":
    run_eval()