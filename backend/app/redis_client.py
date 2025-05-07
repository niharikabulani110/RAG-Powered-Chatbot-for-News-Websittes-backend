import redis
import os
from dotenv import load_dotenv

load_dotenv()

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_TTL = int(os.getenv("REDIS_TTL", 86400))  # 24 hours default TTL

# Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def _session_key(session_id: str) -> str:
    """Namespaced Redis key for the session."""
    return f"session:{session_id}"

def store_chat(session_id: str, query: str, answer: str):
    key = _session_key(session_id)
    r.rpush(key, f"User: {query}")
    r.rpush(key, f"Bot: {answer}")
    r.expire(key, REDIS_TTL)  # Set/reset TTL on new message

def get_session_history(session_id: str):
    key = _session_key(session_id)
    return r.lrange(key, 0, -1)

def clear_session(session_id: str):
    key = _session_key(session_id)
    r.delete(key)
    return {"status": "cleared"}
