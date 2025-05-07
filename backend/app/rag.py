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
        print("Query Vector:", query_vector)  # Debugging log

        # Step 2: Search in Qdrant
        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=3
        )

        print("Qdrant Search Results:", results)  # Debugging log

        if not results:
            return "I couldn't find any relevant articles to answer your question."

        # Step 3: Build context from top results
        context = "\n\n".join([r.payload["text"] for r in results])
        print("Context:", context)  # Debugging log

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
        print("Gemini Response:", response)  # Debugging log
        answer = response.text.strip()

        # Step 6: Store in Redis
        store_chat(session_id, query, answer)
        print(f"Storing in Redis: {session_id}, {query}, {answer}")  # Debugging log

        return answer

    except Exception as e:
        print("Gemini API Error:\n", traceback.format_exc())
        print("Error Details:", str(e))  # Log error details
        return "Sorry, I encountered an error while fetching the answer."
