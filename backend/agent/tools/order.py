"""
order — Tools: check_stock, create_order

Kiểm tra tồn kho và tạo đơn hàng từ lựa chọn của khách hàng.
"""
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from .data_loader import (
    _get_merchant,
    _find_item_by_name,
    _extract_selections_from_text,
)


def _resolve_selections(
    merchant: Dict[str, Any],
    selections: Optional[List[Dict[str, Any]]],
    order_text: Optional[str],
) -> Optional[List[Dict[str, Any]]]:
    """Normalise user input into a list of {item_name, quantity}."""
    if selections:
        return selections
    parsed = _extract_selections_from_text(merchant, order_text or "")
    return parsed or None


def _validate_items(merchant: Dict[str, Any], selections: List[Dict[str, Any]]):
    """
    Validate each selection against the menu.
    Returns (resolved, not_found, ambiguous, out_of_stock, insufficient).
    """
    resolved: List[Dict[str, Any]] = []
    not_found: List[str] = []
    ambiguous: List[Dict[str, Any]] = []
    out_of_stock: List[str] = []
    insufficient: List[Dict[str, Any]] = []

    for sel in selections:
        name = sel.get("item_name", "")
        qty = sel.get("quantity", 1)
        if qty is None or qty <= 0:
            qty = 1

        matches = _find_item_by_name(merchant, name)
        if not matches:
            not_found.append(name)
            continue
        if len(matches) > 1:
            ambiguous.append({"query": name, "matches": [m.get("name") for m in matches]})
            continue

        item = matches[0]
        stock_qty = item.get("quantity")
        is_available = item.get("is_avaiable", False)

        if not is_available or (isinstance(stock_qty, int) and stock_qty <= 0):
            out_of_stock.append(item.get("name"))
            continue

        if isinstance(stock_qty, int) and qty > stock_qty:
            insufficient.append({"name": item.get("name"), "requested": qty, "available": stock_qty})
            continue

        resolved.append({"item": item, "quantity": qty})

    return resolved, not_found, ambiguous, out_of_stock, insufficient


def _format_errors(not_found, ambiguous, out_of_stock, insufficient, cta: str) -> str:
    """Build a Vietnamese error summary string."""
    lines = []
    if not_found:
        lines.append("Không tìm thấy món: " + ", ".join(n for n in not_found if n))
    if ambiguous:
        lines.append("Món chưa rõ, vui lòng chọn đúng tên:")
        for amb in ambiguous:
            lines.append(f"- '{amb['query']}' có thể là: {', '.join(amb['matches'])}")
    if out_of_stock:
        lines.append("Món tạm hết hàng: " + ", ".join(out_of_stock))
    if insufficient:
        lines.append("Số lượng yêu cầu vượt tồn kho:")
        for it in insufficient:
            lines.append(f"- {it['name']}: yêu cầu {it['requested']}, còn {it['available']}")
    lines.append(cta)
    return "\n".join(lines)


@tool
def check_stock(
    merchant_id: str,
    selections: Optional[List[Dict[str, Any]]] = None,
    order_text: Optional[str] = None,
) -> str:
    """
    Check remaining stock for items before creating an order.
    selections: list of { "item_name": str, "quantity": int }
    order_text: optional raw user text to extract selections if selections is missing.
    """
    if not merchant_id:
        return "Vui lòng cung cấp merchant_id."

    merchant = _get_merchant(merchant_id)
    if not merchant:
        return f"Merchant with ID {merchant_id} not found."

    sels = _resolve_selections(merchant, selections, order_text)
    if not sels:
        return "Vui lòng cung cấp danh sách món và số lượng (selections)."

    resolved, not_found, ambiguous, out_of_stock, insufficient = _validate_items(merchant, sels)

    if not_found or ambiguous or out_of_stock or insufficient:
        return _format_errors(
            not_found, ambiguous, out_of_stock, insufficient,
            "Bạn vui lòng chỉnh lại số lượng hoặc chọn món khác nhé.",
        )

    return "Tồn kho đủ để tạo đơn."


@tool
def create_order(
    merchant_id: str,
    selections: Optional[List[Dict[str, Any]]] = None,
    order_text: Optional[str] = None,
) -> str:
    """
    Create an order from user's natural-language selections.
    selections: list of { "item_name": str, "quantity": int }
    order_text: optional raw user text to extract selections if selections is missing.
    """
    if not merchant_id:
        return "Vui lòng cung cấp merchant_id."

    merchant = _get_merchant(merchant_id)
    if not merchant:
        return f"Merchant with ID {merchant_id} not found."

    sels = _resolve_selections(merchant, selections, order_text)
    if not sels:
        return "Vui lòng cung cấp danh sách món và số lượng (selections)."

    resolved, not_found, ambiguous, out_of_stock, insufficient = _validate_items(merchant, sels)

    if not_found or ambiguous or out_of_stock or insufficient:
        return _format_errors(
            not_found, ambiguous, out_of_stock, insufficient,
            "Bạn vui lòng chọn lại giúp mình nhé.",
        )

    total = 0
    lines = ["Đơn hàng tạm tính:"]
    for r in resolved:
        item = r["item"]
        qty = r["quantity"]
        line_total = item["price"] * qty
        total += line_total
        lines.append(f"- {item['name']} x{qty}: {line_total} VND")

    lines.append(f"Tổng cộng: {total} VND")
    lines.append("Bạn xác nhận đặt đơn này chứ?")
    return "\n".join(lines)
