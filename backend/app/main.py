from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from app.rag import ask_question
from app.redis_client import get_session_history, clear_session
from app.models import ChatRequest
import uuid
import logging

# Set up logging to capture debug info
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# List of allowed origins (frontend URL)
origins = [
    "http://localhost:5173",  # Frontend URL (adjust if different)
]

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/chat")
async def chat(req: ChatRequest):
    # Debugging logs to track the query and session ID
    logger.debug(f"Received query: {req.query}")
    
    # Generate session ID if not provided
    session_id = req.session_id or str(uuid.uuid4())
    logger.debug(f"Using session ID: {session_id}")
    
    try:
        # Call the ask_question function to generate a response
        response = ask_question(req.query, session_id)
        logger.debug(f"Response from ask_question: {response}")
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
