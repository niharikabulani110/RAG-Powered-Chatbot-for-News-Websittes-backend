from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.rag import ask_question
from app.redis_client import get_session_history, clear_session
from app.models import ChatRequest
from app.db import save_transcript, init_db  # Added DB support
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Allow frontend origin
origins = [
    "http://localhost:5173",  # Update if deployed to another URL
]

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB tables at startup
init_db()

@app.post("/chat")
async def chat(req: ChatRequest):
    logger.debug(f"Received query: {req.query}")
    
    session_id = req.session_id or str(uuid.uuid4())
    logger.debug(f"Using session ID: {session_id}")

    try:
        # Call RAG pipeline
        response = ask_question(req.query, session_id)
        logger.debug(f"Response from ask_question: {response}")

        # Save to optional SQL DB
        save_transcript(session_id, req.query, response)

    except Exception as e:
        logger.error(f"Error during ask_question: {e}")
        response = "Sorry, I encountered an error while fetching the answer."
    
    return {"answer": response, "session_id": session_id}

@app.get("/history/{session_id}")
def get_history(session_id: str):
    logger.debug(f"Fetching history for session: {session_id}")
    return get_session_history(session_id)

@app.post("/reset/{session_id}")
def reset(session_id: str):
    logger.debug(f"Resetting session: {session_id}")
    return clear_session(session_id)
