import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", BASE_DIR / "data" / "mock"))

MENU_DATA_PATH = DATA_DIR / "menus" / "store_001.json"
FEEDBACK_FILE = DATA_DIR / "merchant_feedback.json"
EVAL_LOGS_FILE = DATA_DIR / "merchant_eval_logs.json"
