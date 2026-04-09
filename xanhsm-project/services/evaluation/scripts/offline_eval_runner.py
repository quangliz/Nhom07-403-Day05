import json, os, time, sys
import httpx
from pathlib import Path

# Paths & URLs
ROOT_DIR = Path(__file__).parent.parent.parent.parent
GT_PATH = ROOT_DIR / "data" / "mock" / "ground_truth" / "qa_pairs.json"
AGENT_URL = os.environ.get("AGENT_URL", "http://localhost:8000") # Run from local
EVAL_URL  = os.environ.get("EVAL_URL", "http://localhost:8002")

UNSURE_KEYWORDS = ["không chắc", "chưa cung cấp", "không có thông tin", "liên hệ quán", "vui lòng liên hệ"]

def check_answer(ai_resp: str, qa: dict):
    r = ai_resp.lower()
    is_unsure = any(k in r for k in UNSURE_KEYWORDS)
    
    expected_contains = qa.get("expected_answer_contains", [])
    expected_not_contains = qa.get("expected_answer_not_contains", [])
    
    # Neu AI chon pass "khong chac chan"
    if is_unsure:
        if qa.get("expected_confidence") == "unsure":
            return True, "Correctly identified as unsure", True # passed, reason, is_unsure
        else:
            return False, "False Negative: AI declined to answer but should have", True

    for kw in expected_contains:
        if kw.lower() not in r: 
            return False, f"Missing expected keyword: '{kw}'", False
    
    for kw in expected_not_contains:
        if kw.lower() in r: 
            return False, f"Contains forbidden keyword: '{kw}'", False

    if qa.get("expected_confidence") == "unsure" and not is_unsure:
        return False, "False Positive: AI hallucinated / acted confident without data", False

    return True, "Exact Match", False

def run_offline_eval():
    if not GT_PATH.exists():
        print(f"Error: {GT_PATH} not found!")
        sys.exit(1)
        
    with open(GT_PATH, encoding="utf-8") as f:
        qa_pairs = json.load(f)
        
    print(f"Loaded {len(qa_pairs)} QA pairs. Starting evaluation...")
    
    results = []
    
    total = len(qa_pairs)
    unsure_count = 0 
    correct_count = 0
    false_positives = 0
    false_negatives = 0
    
    with httpx.Client(timeout=30) as client:
        for i, qa in enumerate(qa_pairs):
            print(f"Testing [{i+1}/{total}]: {qa['question']}")
            t0 = time.time()
            try:
                res = client.post(f"{AGENT_URL}/chat", json={
                    "merchant_id": qa["store_id"],
                    "session_id": f"offline_eval_{int(time.time())}",
                    "message": qa["question"]
                })
                res.raise_for_status()
                ai_resp = res.json().get("response", "")
            except Exception as e:
                print(f"  -> Agent failed: {e}")
                results.append({"id": qa["id"], "error": str(e)})
                continue
                
            latency = time.time() - t0
            passed, reason, is_unsure = check_answer(ai_resp, qa)
            
            if passed: correct_count += 1
            if is_unsure: unsure_count += 1
            
            if not passed and not is_unsure: false_positives += 1
            if not passed and is_unsure: false_negatives += 1
            
            print(f"  -> Passed: {passed} | Unsure: {is_unsure} | Latency: {latency:.2f}s")
            
            results.append({
                "id": qa["id"],
                "question": qa["question"],
                "latency_s": latency,
                "passed": passed,
                "is_unsure": is_unsure,
                "reason": reason,
                "ai_resp": ai_resp
            })
            
    # Calculate Metrics
    precision = correct_count / (total - unsure_count) if (total - unsure_count) > 0 else 1.0
    answer_rate = (total - unsure_count) / total if total > 0 else 0
    accuracy = correct_count / total if total > 0 else 0
    
    print("\n" + "="*40)
    print("OFFLINE EVALUATION RESULTS")
    print("="*40)
    print(f"Total QA Pairs    : {total}")
    print(f"Total Correct     : {correct_count}")
    print(f"Answer Rate       : {answer_rate:.2%}")
    print(f"Precision         : {precision:.2%}")
    print(f"Accuracy          : {accuracy:.2%}")
    print(f"False Positives   : {false_positives} (Critical Danger)")
    print(f"False Negatives   : {false_negatives} (Lost Opportunities)")
    print("="*40)
    
    # Save report
    report_file = Path(__file__).parent / f"eval_report_{int(time.time())}.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "metrics": {
                "total": total,
                "correct": correct_count,
                "accuracy": accuracy,
                "precision": precision,
                "answer_rate": answer_rate,
                "false_positives": false_positives,
                "false_negatives": false_negatives
            },
            "details": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nReport saved to: {report_file}")

if __name__ == "__main__":
    run_offline_eval()
