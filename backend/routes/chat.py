from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import time
import uuid
import threading
import logging
from langchain_core.messages import HumanMessage
from agent.core import MerchantAgent, USER_MEMORIES
from agent.tools import get_all_merchants
from config import EVAL_LOGS_FILE
from langgraph.checkpoint.memory import MemorySaver
from ._eval_log import send_eval_log

router = APIRouter()
logger = logging.getLogger("api.chat")

agents: Dict[str, MerchantAgent] = {}
memory = MemorySaver()


class ChatRequest(BaseModel):
    merchant_id: str
    message: str
    session_id: str = "default_session"
    user_id: str = "default_user"


class ActionButton(BaseModel):
    label: str
    action: str
    payload: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    log_id: str
    message: str
    merchant_name: str
    confidence: str = "high"
    action_buttons: Optional[List[ActionButton]] = None
    latency_ms: float
    total_tokens: int
    tool_debug_info: Optional[List[Dict[str, Any]]] = None


@router.get("/merchants")
def list_merchants():
    """Return a list of all available merchants."""
    return get_all_merchants()


@router.get("/memory/{user_id}")
def get_user_memory(user_id: str):
    """Retrieve saved memory for a given user ID."""
    memories = USER_MEMORIES.get(user_id, [])
    return {"user_id": user_id, "memories": memories}


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """Chat with a specific merchant's AI assistant."""
    logger.info(f"Processing chat request for merchant: {request.merchant_id}, user: {request.user_id}")
    merchants = get_all_merchants()
    merchant = next((m for m in merchants if m["id"] == request.merchant_id), None)

    if not merchant:
        logger.warning(f"Merchant not found: {request.merchant_id}")
        raise HTTPException(status_code=404, detail="Merchant not found")

    if request.merchant_id not in agents:
        agents[request.merchant_id] = MerchantAgent(request.merchant_id, checkpointer=memory)

    agent = agents[request.merchant_id]

    config = {"configurable": {"thread_id": request.session_id, "user_id": request.user_id}}
    start_time = time.time()
    try:
        state = agent.invoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config,
        )
    except Exception as e:
        logger.error(f"Error in agent execution for merchant {request.merchant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    latency_ms = (time.time() - start_time) * 1000

    messages = state["messages"]
    ai_response = messages[-1].content

    tools_called = []
    token_usage = {}
    for i, msg in enumerate(messages):
        if getattr(msg, "type", "") == "ai":
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    tool_output = "No output found"
                    if i + 1 < len(messages) and getattr(messages[i + 1], "type", "") == "tool":
                        tool_output = messages[i + 1].content
                    tools_called.append({
                        "name": tc["name"],
                        "args": tc["args"],
                        "output": tool_output,
                    })
            if hasattr(msg, "response_metadata") and "token_usage" in msg.response_metadata:
                token_usage = msg.response_metadata["token_usage"]

    log_id = str(uuid.uuid4())

    threading.Thread(target=send_eval_log, args=({
        "log_id": log_id,
        "merchant_id": request.merchant_id,
        "session_id": request.session_id,
        "user_id": request.user_id,
        "query": request.message,
        "response_text": ai_response,
        "tools_called": tools_called,
        "token_usage": token_usage,
        "latency_ms": latency_ms,
        "confidence": "high",
    },), daemon=True).start()

    action_buttons = [
        ActionButton(label="👍", action="like", payload={"query": request.message}),
        ActionButton(label="👎", action="dislike", payload={"query": request.message}),
    ]

    logger.info(f"Chat response generated for {request.user_id} in {latency_ms:.2f}ms")
    return ChatResponse(
        log_id=log_id,
        message=ai_response,
        merchant_name=merchant["name"],
        confidence="high",
        action_buttons=action_buttons,
        latency_ms=round(latency_ms, 2),
        total_tokens=token_usage.get("total_tokens", 0),
        tool_debug_info=tools_called,
    )
