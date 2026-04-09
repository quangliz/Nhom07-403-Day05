import json, os, httpx
from pathlib import Path

GT_PATH    = Path(os.environ.get("GROUND_TRUTH_PATH","/app/data/mock/ground_truth/qa_pairs.json"))
AGENT_URL  = os.environ.get("AGENT_URL","http://ai-agent:8000")
DISCLAIMER = ["xin xác nhận","ai có thể có lỗi","liên hệ quán","kiểm tra kỹ","vui lòng xác nhận"]
UNSURE     = ["không chắc","chưa cung cấp","không có thông tin","liên hệ","chưa có thông tin"]

def _has_disclaimer(t): return any(p in t.lower() for p in DISCLAIMER)

def _check(response: str, qa: dict):
    r = response.lower()
    for kw in qa.get("expected_answer_contains",[]):
        if kw.lower() not in r: return False, f"Thiếu keyword: '{kw}'"
    for kw in qa.get("expected_answer_not_contains",[]):
        if kw.lower() in r: return False, f"Chứa keyword cấm: '{kw}'"
    if qa.get("expected_confidence")=="unsure":
        if not any(p in r for p in UNSURE): return False, "Thiếu unsure signal"
    if qa.get("requires_disclaimer") and not _has_disclaimer(response):
        return False, "Thiếu disclaimer allergen"
    return True, "ok"

def run_accuracy_eval(logs: list) -> dict:
    if not GT_PATH.exists(): return {"error":"Ground truth not found","accuracy":None}
    with open(GT_PATH,encoding="utf-8") as f: qa_pairs=json.load(f)
    if not qa_pairs or not logs: return {"accuracy":None,"total_qa":len(qa_pairs),"matched":0,"threshold":0.92,"passing":False,"details":[]}
    matched, details = 0, []
    for qa in qa_pairs:
        mid=qa.get("merchant_id",""); kws=qa["question"].lower().split()
        best_log, best_score = None, 0
        for log in logs:
            if log.get("merchant_id")!=mid: continue
            score=sum(1 for kw in kws if kw in log.get("query","").lower())
            if score>best_score: best_score,best_log=score,log
        passed,reason = _check(best_log.get("response_text",""),qa) if best_log else (False,"No matching log")
        if passed: matched+=1
        details.append({"qa_id":qa["id"],"question":qa["question"],"merchant_id":mid,"passed":passed,"reason":reason})
    acc=round(matched/len(qa_pairs),4)
    return {"accuracy":acc,"accuracy_pct":round(acc*100,2),"total_qa":len(qa_pairs),"matched":matched,"threshold":0.92,"passing":acc>=0.92,"details":details}

def run_batch_accuracy(session_id="eval_batch") -> dict:
    if not GT_PATH.exists(): return {"error":"Ground truth not found"}
    with open(GT_PATH,encoding="utf-8") as f: qa_pairs=json.load(f)
    matched, details = 0, []
    with httpx.Client(timeout=30) as client:
        for qa in qa_pairs:
            try:
                r=client.post(f"{AGENT_URL}/chat",json={"merchant_id":qa["merchant_id"],"message":qa["question"],"session_id":session_id})
                r.raise_for_status(); ai_resp=r.json().get("message","")
                passed,reason=_check(ai_resp,qa)
            except Exception as e: ai_resp=""; passed,reason=False,f"Agent error: {e}"
            if passed: matched+=1
            details.append({"qa_id":qa["id"],"question":qa["question"],"merchant_id":qa["merchant_id"],"ai_response":ai_resp[:300],"passed":passed,"reason":reason})
    acc=round(matched/len(qa_pairs),4) if qa_pairs else 0
    return {"accuracy":acc,"accuracy_pct":round(acc*100,2),"total_qa":len(qa_pairs),"matched":matched,"threshold":0.92,"passing":acc>=0.92,"details":details}

def check_disclaimer_compliance(logs: list) -> dict:
    allergen=[l for l in logs if l.get("is_allergen_query")]
    if not allergen: return {"disclaimer_rate":None,"total_allergen_queries":0,"threshold":0.95,"passing":True}
    wd=sum(1 for l in allergen if l.get("has_disclaimer"))
    rate=round(wd/len(allergen),4)
    return {"disclaimer_rate":rate,"disclaimer_rate_pct":round(rate*100,2),"total_allergen_queries":len(allergen),"with_disclaimer":wd,"without_disclaimer":len(allergen)-wd,"threshold":0.95,"passing":rate>=0.95,"red_flag":rate<0.95}
