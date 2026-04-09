from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import time
import os
import json
import logging
from config import FEEDBACK_FILE

router = APIRouter()
logger = logging.getLogger("api.feedback")


class FeedbackRequest(BaseModel):
    log_id: str
    merchant_id: str
    signal_type: str  # 'positive', 'implicit_negative', 'explicit_negative'
    details: Optional[str] = None


@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    """Store explicit or implicit user feedback into the correction log."""
    logger.info(f"Receiving feedback: {request.signal_type} for log_id: {request.log_id}")
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            feedbacks = json.load(f)
    except FileNotFoundError:
        feedbacks = []

    feedbacks.append(request.model_dump() | {"timestamp": time.time()})

    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=2)

    logger.info("Feedback successfully recorded.")
    return {"status": "success", "message": "Feedback recorded."}


@router.get("/merchant/{merchant_id}/feedback")
def get_merchant_feedback(merchant_id: str):
    """List all feedbacks for a merchant."""
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            feedbacks = json.load(f)
        return [fb for fb in feedbacks if fb.get("merchant_id") == merchant_id]
    except FileNotFoundError:
        return []
