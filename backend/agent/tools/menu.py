"""
menu — Tool: list_items

Tìm kiếm và lọc món ăn trong thực đơn của quán.
Hỗ trợ tìm theo tên, giá tối đa, loại trừ nguyên liệu, và chọn trường trả về.
"""
from typing import List, Optional, Literal
from langchain_core.tools import tool
from .data_loader import _get_merchant


@tool
def list_items(
    merchant_id: str,
    search_term: Optional[str] = None,
    max_price: Optional[int] = None,
    exclude_ingredients: Optional[List[str]] = None,
    return_fields: Optional[
        List[Literal["name", "price", "description", "ingredients", "is_avaiable"]]
    ] = None,
) -> str:
    """
    List dishes from the merchant's menu based on specific filters.
    Use this to search for items, recommend dishes, or check ingredients.
    Arguments:
        merchant_id: The ID of the merchant.
        search_term: (Optional) Search query for dish name or feature (e.g. 'cơm', 'cay').
        max_price: (Optional) Maximum price in VND (e.g. 100000).
        exclude_ingredients: (Optional) List of ingredients to avoid (e.g. ["bò", "tôm"]).
        return_fields: (Optional) List of specific fields to return (e.g. ["name", "price"]).
                       If not provided, returns all fields.
    This will return matching items with the requested fields.
    Items marked as 'is_avaiable' = False are temporarily out of stock.
    """
    if not merchant_id:
        return "Vui lòng cung cấp merchant_id."

    merchant = _get_merchant(merchant_id)
    if not merchant:
        return f"Merchant with ID {merchant_id} not found."

    results = []
    search_lower = search_term.lower() if search_term else None

    for item in merchant.get("items", []):
        # 1. Price filter
        if max_price is not None and item["price"] > max_price:
            continue

        # 2. Ingredient exclusion filter
        if exclude_ingredients:
            exclude = False
            desc_lower = (item["description"] or "").lower()
            name_lower = item["name"].lower()
            ings = [ing.lower() for ing in item.get("ingredients", [])]

            for exc in exclude_ingredients:
                exc_lower = exc.lower()
                if (
                    exc_lower in name_lower
                    or exc_lower in desc_lower
                    or any(exc_lower in ing for ing in ings)
                ):
                    exclude = True
                    break
            if exclude:
                continue

        # 3. Search term filter (with Vietnamese normalization)
        if search_lower:
            desc_lower = (item["description"] or "").lower()
            name_lower = item["name"].lower()
            ings = [ing.lower() for ing in item.get("ingredients", [])]

            search_normalized = search_lower.replace("mỳ", "mì")
            name_normalized = name_lower.replace("mỳ", "mì")
            desc_normalized = desc_lower.replace("mỳ", "mì")

            search_words = search_normalized.split()

            match = True
            for word in search_words:
                word_match = False
                if word in name_normalized or word in desc_normalized:
                    word_match = True
                elif any(word in ing.replace("mỳ", "mì") for ing in ings):
                    word_match = True

                if not word_match:
                    match = False
                    break

            if not match:
                continue

        # Build response based on requested fields
        fields_to_return = return_fields if return_fields is not None else [
            "name", "price", "description", "ingredients", "is_avaiable"
        ]

        item_strs = [f"- Tên món: {item['name']}"]  # Always include name

        if "price" in fields_to_return:
            item_strs.append(f"  Giá: {item['price']} VND")
        if "description" in fields_to_return:
            item_strs.append(f"  Mô tả: {item['description']}")
        if "ingredients" in fields_to_return:
            ing_str = (
                ", ".join(item.get("ingredients", []))
                if item.get("ingredients")
                else "Không có thông tin nguyên liệu"
            )
            item_strs.append(f"  Nguyên liệu: {ing_str}")
        if "is_avaiable" in fields_to_return:
            avail = (
                "Có sẵn"
                if item.get("is_avaiable")
                else "TẠM HẾT HÀNG (Không được đề xuất)"
            )
            item_strs.append(f"  Tình trạng: {avail}")

        results.append("\n".join(item_strs))

    if not results:
        return "Không tìm thấy món nào thỏa mãn các điều kiện."

    return "\n\n".join(results)
