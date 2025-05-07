from fastapi import FastAPI, Request
from app.rag import ask_question
from app.redis_client import get_session_history, clear_session
from app.models import ChatRequest
import uuid

app = FastAPI()

@app.post("/chat")
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    response = ask_question(req.query, session_id)
    return {"answer": response, "session_id": session_id}

@app.get("/history/{session_id}")
def get_history(session_id: str):
    return get_session_history(session_id)

@app.post("/reset/{session_id}")
def reset(session_id: str):
    return clear_session(session_id)
