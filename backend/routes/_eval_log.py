import json
import os
import logging
from config import EVAL_LOGS_FILE

logger = logging.getLogger("api.eval_log")


def send_eval_log(payload: dict):
    """Persist an eval log entry locally (fire-and-forget from chat endpoint)."""
    try:
        os.makedirs(os.path.dirname(EVAL_LOGS_FILE), exist_ok=True)
        try:
            with open(EVAL_LOGS_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
        logs.append(payload)
        with open(EVAL_LOGS_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to persist eval log: {e}")
