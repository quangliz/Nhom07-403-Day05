"""
faq — Tool: get_faq

Trả lời các câu hỏi thường gặp (FAQ), chính sách, giờ mở cửa, v.v.
"""
from langchain_core.tools import tool
from .data_loader import _get_merchant


@tool
def get_faq(merchant_id: str) -> str:
    """
    Fetch FAQs (frequently asked questions) and general policies/notes for a specific merchant.
    Use this when the user asks about packaging, rules, operating hours, tools, or policies.
    """
    merchant = _get_merchant(merchant_id)
    if not merchant:
        return f"Merchant with ID {merchant_id} not found."

    info = f"Lưu ý từ quán: {merchant['description']}\n\n"
    info += "Các câu hỏi thường gặp (FAQ):\n"
    for faq in merchant.get("faqs", []):
        info += f"Q: {faq['question']}\n"
        info += f"A: {faq['answer']}\n\n"

    return info
