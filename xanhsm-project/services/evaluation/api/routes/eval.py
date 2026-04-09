from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
<<<<<<< HEAD
from logger import write_log, update_outcome, write_correction, load_logs, load_corrections
from metrics.accuracy  import run_accuracy_eval, run_batch_accuracy, check_disclaimer_compliance
from metrics.latency   import compute_p95_latency
from metrics.conversion import compute_conversion_rate, compute_satisfaction_rate, compute_unsure_rate
=======
from logger import write_log, update_outcome, write_correction
>>>>>>> e370928 (add tools, refactor code)

router = APIRouter()

class EvalLogRequest(BaseModel):
    merchant_id: str
    session_id: str
    query: str
    intent: str = "unknown"
    tools_called: list = []
    response_text: str
    confidence: str = "high"
    latency_ms: float
    token_usage: Optional[dict] = None

class OutcomeRequest(BaseModel):
    log_id: str
    outcome: str  # "converted" | "reported_wrong" | "ignored"

class CorrectionRequest(BaseModel):
    log_id: str
    item_id: str
    reason: str
    user_note: Optional[str] = None

@router.post("/eval/log")
async def log_eval(req: EvalLogRequest):
    log_id = write_log(req.model_dump())
    return {"log_id": log_id, "ok": True}

@router.post("/eval/outcome")
async def log_outcome(req: OutcomeRequest):
    found = update_outcome(req.log_id, req.outcome)
    return {"ok": found, "log_id": req.log_id, "outcome": req.outcome}

@router.post("/eval/correction")
async def log_correction(req: CorrectionRequest):
    cid = write_correction(req.model_dump())
    return {"ok": True, "correction_id": cid, "message": "Merchant đã được notify."}

@router.get("/eval/dashboard")
async def dashboard(days: int = Query(7, ge=1, le=30)):
    logs = load_logs(days=days)
    latency      = compute_p95_latency(logs)
    conversion   = compute_conversion_rate(logs)
    satisfaction = compute_satisfaction_rate(logs)
    disclaimer   = check_disclaimer_compliance(logs)
    unsure       = compute_unsure_rate(logs)
    accuracy     = run_accuracy_eval(logs)
    kill = []
    if conversion.get("red_flag"):   kill.append("❌ Conversion < 15%")
    if unsure.get("stop_immediately"): kill.append("🛑 STOP: Hallucination allergen > 10%")
    if latency.get("red_flag"):      kill.append("⚠️ Latency p95 > 15s")
    return {
        "period_days": days, "total_queries": len(logs),
        "metrics": {"accuracy":accuracy,"latency":latency,"conversion":conversion,
                    "satisfaction":satisfaction,"disclaimer_compliance":disclaimer,"allergen_hallucination":unsure},
        "kill_criteria_triggered": kill,
        "status": "🛑 STOP" if unsure.get("stop_immediately") else ("⚠️ WARNING" if kill else "✅ OK"),
    }

@router.get("/eval/logs")
async def get_logs(days: int = Query(1,ge=1,le=7), merchant_id: Optional[str]=None, limit: int=Query(50,ge=1,le=500)):
    logs = load_logs(days=days)
    if merchant_id: logs=[l for l in logs if l.get("merchant_id")==merchant_id]
    return {"total": len(logs), "logs": logs[-limit:]}

@router.get("/eval/corrections")
async def get_corrections(limit: int = Query(50,ge=1,le=200)):
    c = load_corrections(limit=limit)
    return {"total": len(c), "corrections": c}

@router.post("/eval/accuracy/run")
async def run_accuracy(session_id: str = "eval_batch_001"):
    return run_batch_accuracy(session_id=session_id)
