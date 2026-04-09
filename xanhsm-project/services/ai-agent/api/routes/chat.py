from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from langchain_core.messages import HumanMessage
from agent.core import create_merchant_agent, get_all_merchants
from langgraph.checkpoint.memory import MemorySaver

app = FastAPI(title="Merchant Chatbot API", description="A simple API for the LangGraph agent")

# Global dict to hold one agent instance per merchant
agents = {}
# Single memory store for all sessions
memory = MemorySaver()

class ChatRequest(BaseModel):
    merchant_id: str
    message: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    response: str
    merchant_name: str

@app.get("/merchants")
def list_merchants():
    """Return a list of all available merchants."""
    return get_all_merchants()

@app.post("/chat", response_model=ChatResponse)
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
    state = agent.invoke(
        {"messages": [HumanMessage(content=request.message)]}, 
        config=config
    )
    
    ai_response = state["messages"][-1].content
    
    return ChatResponse(
        response=ai_response,
        merchant_name=merchant["name"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)