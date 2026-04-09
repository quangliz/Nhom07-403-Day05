"""
data_loader — Shared data access layer for merchant/menu data.

Loads merchant data from the central mock JSON and provides
lookup helpers used by all tool modules.
"""
import json
import re
from typing import List, Dict, Any, Optional
from config import MENU_DATA_PATH

DATA_PATH = str(MENU_DATA_PATH)


def _load_data() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    # Support both list format and {"merchants": [...]} format
    if isinstance(raw, list):
        return raw
    return raw.get("merchants", [])


def get_all_merchants() -> List[Dict[str, Any]]:
    """Return every merchant entry (id, name, description, items, faqs)."""
    return _load_data()


def _get_merchant(merchant_id: str) -> Optional[Dict[str, Any]]:
    """Find a single merchant by ID, or None."""
    for merchant in _load_data():
        if merchant["id"] == merchant_id:
            return merchant
    return None


# ── Text helpers (used by order tools) ──────────────────────────────

def _normalize_text(text: str) -> str:
    return (text or "").strip().lower()


def _name_variants(name: str) -> List[str]:
    """Generate search-friendly variants of a dish name."""
    base = _normalize_text(name)
    variants = [base]
    if "(" in base and ")" in base:
        variants.append(_normalize_text(base.split("(")[0].strip()))
    tokens = base.split()
    if len(tokens) >= 2:
        variants.append(" ".join(tokens[:2]))
    return list(dict.fromkeys([v for v in variants if v]))


def _find_item_by_name(merchant: Dict[str, Any], item_name: str) -> List[Dict[str, Any]]:
    """Fuzzy-match an item name against a merchant's menu."""
    target = _normalize_text(item_name)
    if not target:
        return []

    items = merchant.get("items", [])
    exact = [it for it in items if _normalize_text(it.get("name", "")) == target]
    if exact:
        return exact

    return [it for it in items if target in _normalize_text(it.get("name", ""))]


def _extract_selections_from_text(
    merchant: Dict[str, Any], order_text: str
) -> List[Dict[str, Any]]:
    """Parse Vietnamese order text into [{item_name, quantity}, ...]."""
    text = _normalize_text(order_text)
    if not text:
        return []

    selections: List[Dict[str, Any]] = []
    for item in merchant.get("items", []):
        name = item.get("name", "")
        variants = _name_variants(name)
        matched = False
        qty_found = None

        for v in variants:
            if not v:
                continue
            if v in text:
                matched = True
                pattern1 = rf"(\d+)\s*(phần|suất|tô|bát|dĩa|đĩa)?\s*{re.escape(v)}"
                pattern2 = rf"{re.escape(v)}\s*(\d+)"
                m = re.search(pattern1, text)
                if m:
                    qty_found = int(m.group(1))
                else:
                    m = re.search(pattern2, text)
                    if m:
                        qty_found = int(m.group(1))
                break

        if matched:
            selections.append({
                "item_name": name,
                "quantity": qty_found if qty_found and qty_found > 0 else 1,
            })

    return selections
