from fastapi import APIRouter
import json
import logging
from config import EVAL_LOGS_FILE, FEEDBACK_FILE

router = APIRouter()
logger = logging.getLogger("api.analytics")


@router.get("/merchant/{merchant_id}/analytics")
def get_merchant_analytics(merchant_id: str):
    """Calculates metrics dynamically from real evaluation and feedback logs."""
    logger.info(f"Calculating analytics for merchant: {merchant_id}")

    try:
        with open(EVAL_LOGS_FILE, "r", encoding="utf-8") as f:
            eval_logs = [log for log in json.load(f) if log.get("merchant_id") == merchant_id]
    except (FileNotFoundError, json.JSONDecodeError):
        eval_logs = []

    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            feedbacks = [fb for fb in json.load(f) if fb.get("merchant_id") == merchant_id]
    except (FileNotFoundError, json.JSONDecodeError):
        feedbacks = []

    total_chats = len(eval_logs)
    if total_chats == 0:
        logger.info(f"No analytics data for merchant: {merchant_id}")
        return {"merchant_id": merchant_id, "total_chats": 0}

    total_latency = sum(log.get("latency_ms", 0) for log in eval_logs)
    total_tokens = sum(log.get("token_usage", {}).get("total_tokens", 0) for log in eval_logs)

    cost = total_tokens * 0.0000001

    positive_feedback = len([fb for fb in feedbacks if fb.get("signal_type") == "positive"])
    negative_feedback = len([fb for fb in feedbacks if fb.get("signal_type") == "explicit_negative"])

    total_feedback = positive_feedback + negative_feedback
    analytics = {
        "merchant_id": merchant_id,
        "avg_latency_ms": round(total_latency / total_chats, 2),
        "avg_cost_per_chat": round(cost / total_chats, 6),
        "conversion_rate": round(positive_feedback / total_chats, 2),
        "total_chats": total_chats,
        "satisfaction_score": round(positive_feedback / total_feedback if total_feedback > 0 else 0.0, 2),
    }
    logger.info(f"Analytics returned for merchant: {merchant_id}")
    return analytics
