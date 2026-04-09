from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import time, os, httpx
from langchain_core.messages import HumanMessage
from agent.core import create_merchant_agent
from tools import get_all_merchants
from langgraph.checkpoint.memory import MemorySaver

router = APIRouter()

# Global dict to hold one agent instance per merchant
agents = {}
# Single memory store for all sessions
memory = MemorySaver()

EVAL_SERVICE_URL = os.environ.get("EVAL_SERVICE_URL", "http://evaluation:8002")

def send_eval_log(payload: dict):
    try:
        with httpx.Client(timeout=5) as client:
            client.post(f"{EVAL_SERVICE_URL}/eval/log", json=payload)
    except Exception as e:
        print(f"Failed to push eval log: {e}")

class ChatRequest(BaseModel):
    merchant_id: str
    message: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    response: str
    merchant_name: str

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """Chat with a specific merchant's AI assistant."""
    merchants = get_all_merchants()
    merchant = next((m for m in merchants if m["id"] == request.merchant_id), None)
    
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
        
    # Instantiate the agent for this merchant if we haven't already
    if request.merchant_id not in agents:
        agents[request.merchant_id] = create_merchant_agent(request.merchant_id, checkpointer=memory)
        
    agent = agents[request.merchant_id]
    
    # Run the agent graph
    config = {"configurable": {"thread_id": request.session_id}}
    start_time = time.time()
    state = agent.invoke(
        {"messages": [HumanMessage(content=request.message)]}, 
        config=config
    )
    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000
    
    messages = state["messages"]
    ai_response = messages[-1].content
    
    # Extract AI tracing info
    tools_called = []
    token_usage = {}
    
    for msg in messages:
        if getattr(msg, "type", "") == "ai":
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    tools_called.append({"name": tc["name"], "args": tc["args"]})
            if hasattr(msg, "response_metadata") and "token_usage" in msg.response_metadata:
                token_usage = msg.response_metadata["token_usage"]
                
    # Push log background task
    log_payload = {
        "merchant_id": request.merchant_id,
        "session_id": request.session_id,
        "query": request.message,
        "response_text": ai_response,
        "tools_called": tools_called,
        "token_usage": token_usage,
        "latency_ms": latency_ms,
        "confidence": "high" # default to high unless unsure
    }
    background_tasks.add_task(send_eval_log, log_payload)
    
    return ChatResponse(
        response=ai_response,
        merchant_name=merchant["name"]
    )
