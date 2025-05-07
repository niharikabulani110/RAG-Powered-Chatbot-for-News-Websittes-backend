import redis
import os
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), decode_responses=True)

def store_chat(session_id: str, query: str, answer: str):
    r.rpush(session_id, f"Q: {query}")
    r.rpush(session_id, f"A: {answer}")

def get_session_history(session_id: str):
    return r.lrange(session_id, 0, -1)

def clear_session(session_id: str):
    r.delete(session_id)
    return {"status": "cleared"}
