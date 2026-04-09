"""
EvalLogger — nhận EvalLog từ AI Agent và persist xuống file/DB
"""
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

LOG_DIR = Path(os.environ.get("LOG_DIR", Path(__file__).parent / "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

_lock = Lock()

DISCLAIMER_KEYWORDS = [
    "xin xác nhận", "ai có thể có lỗi", "liên hệ quán",
    "kiểm tra kỹ", "vui lòng xác nhận",
]
ALLERGEN_KEYWORDS = ["dị ứng", "allergen", "allergy", "di ung"]


def _today_file() -> Path:
    return LOG_DIR / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"


def _has_disclaimer(text: str) -> bool:
    t = text.lower()
    return any(p in t for p in DISCLAIMER_KEYWORDS)


def _is_allergen_query(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in ALLERGEN_KEYWORDS)


def write_log(log: dict) -> str:
    log_id = log.get("log_id") or str(uuid.uuid4())
    resp = log.get("response_text", "")
    record = {
        "log_id": log_id,
        "timestamp": log.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        "merchant_id": log.get("merchant_id", ""),
        "session_id": log.get("session_id", ""),
        "query": log.get("query", ""),
        "intent": log.get("intent", "unknown"),
        "tools_called": log.get("tools_called", []),
        "response_text": resp,
        "confidence": log.get("confidence", "high"),
        "latency_ms": float(log.get("latency_ms", 0)),
        "has_disclaimer": _has_disclaimer(resp),
        "is_allergen_query": _is_allergen_query(log.get("query", "")),
        "token_usage": log.get("token_usage"),
        "outcome": None,
    }
    with _lock:
        with open(_today_file(), "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return log_id


def update_outcome(log_id: str, outcome: str) -> bool:
    for log_file in sorted(LOG_DIR.glob("[0-9]*.jsonl"), reverse=True):
        lines = log_file.read_text(encoding="utf-8").splitlines()
        updated, new_lines = False, []
        for line in lines:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                if r.get("log_id") == log_id:
                    r["outcome"] = outcome
                    updated = True
                new_lines.append(json.dumps(r, ensure_ascii=False))
            except (json.JSONDecodeError, KeyError):
                new_lines.append(line)
        if updated:
            with _lock:
                log_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
            return True
    return False


def write_correction(correction: dict) -> str:
    record = {
        "correction_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **correction,
    }
    with _lock:
        with open(LOG_DIR / "corrections.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record["correction_id"]


def load_logs(days: int = 7) -> list:
    logs = []
    for lf in sorted(LOG_DIR.glob("[0-9]*.jsonl"), reverse=True)[:days]:
        for line in lf.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                logs.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return logs


def load_corrections(limit: int = 100) -> list:
    cf = LOG_DIR / "corrections.jsonl"
    if not cf.exists():
        return []
    rows = []
    for line in cf.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return rows[-limit:]
