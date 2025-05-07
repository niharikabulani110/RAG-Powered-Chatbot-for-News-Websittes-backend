import os
import traceback
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance
import google.generativeai as genai
from app.redis_client import store_chat

# Load environment variables
load_dotenv()

# Constants
COLLECTION_NAME = "news"
QDRANT_URL = os.getenv("QDRANT_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

print("✅ Qdrant URL:", QDRANT_URL)
print("✅ Using Gemini Key (exists):", bool(GOOGLE_API_KEY))

# Initialize services
embedder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(url=QDRANT_URL)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def ask_question(query: str, session_id: str) -> str:
    try:
        # Step 1: Embed the query
        query_vector = embedder.encode([query])[0].tolist()
        print("🧠 Query Vector:", query_vector)

        # Step 2: Retrieve top results from Qdrant
        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=3
        )
        print("🔎 Qdrant Search Results:", results)

        if not results:
            return "I couldn't find any relevant articles to answer your question."

        # Step 3: Build RAG context
        context = "\n\n".join([r.payload.get("text", "") for r in results])
        print("📚 Context passed to Gemini:\n", context)

        # Step 4: Construct the prompt
        prompt = f"""Use the context below to answer the user's question.

Context:
{context}

Question:
{query}
"""

        # Step 5: Generate answer from Gemini
        print("📡 Sending prompt to Gemini...")
        response = model.generate_content(prompt)
        print("✅ Gemini response received")
        answer = response.text.strip()

        # Step 6: Store Q&A in Redis
        store_chat(session_id, query, answer)
        print(f"💾 Stored in Redis: session_id={session_id}")

        return answer

    except Exception as e:
        print("❌ Gemini API Error:\n", traceback.format_exc())
        return "Sorry, I encountered an error while fetching the answer."
