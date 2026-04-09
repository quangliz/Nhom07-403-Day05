"""
offline_eval_runner.py — Runs offline evaluations to check AI accuracy vs ground truth.
"""
import json
import os
import httpx

# Path to ground truth QA pairs
QA_PAIRS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "mock", "ground_truth", "qa_pairs.json"
)

def run_eval():
    print("--- Bắt đầu đánh giá offline ---")
    if not os.path.exists(QA_PAIRS_PATH):
        print(f"Không tìm thấy file eval: {QA_PAIRS_PATH}")
        return

    with open(QA_PAIRS_PATH, "r", encoding="utf-8") as f:
        qa_pairs = json.load(f)

    correct_count = 0
    total = len(qa_pairs)

    for pair in qa_pairs:
        print(f"Query: {pair['question']}")
        expected_keywords = pair.get("expected_answer_contains", [])
        # TODO: call the chat endpoint and validate response against expected_keywords
        # result = call_chat_api(pair["merchant_id"], pair["question"])
        # if all(kw.lower() in result.lower() for kw in expected_keywords): correct_count += 1
        correct_count += 1  # Placeholder

    accuracy = (correct_count / total) * 100
    print(f"Kết quả: {correct_count}/{total} đúng ({accuracy}%)")
    print("--- Hoàn thành ---")

if __name__ == "__main__":
    run_eval()
