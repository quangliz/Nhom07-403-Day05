from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.chat import router as chat_router

app = FastAPI(title="XanhSM AI Agent", version="0.1.0")

# Allow the frontend (local dev + docker-compose) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # local dev
        "http://frontend:3000",    # docker-compose internal
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
