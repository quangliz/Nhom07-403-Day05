from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
import json
import logging
from config import MENU_DATA_PATH

router = APIRouter()
logger = logging.getLogger("api.menu")


class MenuUpdateRequest(BaseModel):
    item_id: str
    field: str
    value: Any


@router.post("/merchant/{merchant_id}/menu/update")
def update_merchant_menu(merchant_id: str, request: MenuUpdateRequest):
    """Updates a specific menu item for a merchant to close the flywheel loop."""
    logger.info(f"Updating menu item {request.item_id} for merchant {merchant_id}")
    with open(MENU_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    merchants = data if isinstance(data, list) else data.get("merchants", [])
    merchant = next((m for m in merchants if m["id"] == merchant_id), None)
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    item = next((i for i in merchant.get("items", []) if i["id"] == request.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item[request.field] = request.value

    with open(MENU_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"Menu item {request.item_id} updated successfully")
    return {"status": "success", "updated_item": item}
