import os
import traceback
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance
import google.generativeai as genai
from app.redis_client import store_chat

# Load .env variables
load_dotenv()

# Constants
COLLECTION_NAME = "news"
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize services
embedder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
genai.configure(api_key=GEMINI_API_KEY)

def ask_question(query: str, session_id: str) -> str:
    try:
        # Step 1: Embed the query
        query_vector = embedder.encode([query])[0].tolist()

        # Step 2: Search in Qdrant
        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=3
        )

        if not results:
            return "I couldn't find any relevant articles to answer your question."

        # Step 3: Build context from top results
        context = "\n\n".join([r.payload["text"] for r in results])

        # Step 4: Build prompt
        prompt = f"""Use the context below to answer the user's question.

Context:
{context}

Question:
{query}
"""

        # Step 5: Generate answer with Gemini
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        answer = response.text.strip()

        # Step 6: Store in Redis
        store_chat(session_id, query, answer)
        return answer

    except Exception:
        print("Gemini API Error:\n", traceback.format_exc())
        return "Sorry, I encountered an error while fetching the answer."
