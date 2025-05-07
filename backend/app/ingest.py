import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
COLLECTION_NAME = "news"
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

# Initialize Qdrant and SentenceTransformer
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Create Qdrant collection if it doesn't exist
if COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # 384 = output dim of the model
    )

def fetch_reuters_articles(limit=10):
    print("[*] Using mock news dataset...")
    return [
        "India announces new trade policy focusing on renewable energy and tech startups.",
        "NASA confirms the Artemis II crew for 2025 lunar flyby mission.",
        "Global markets surge after US Fed hints at slowing interest rate hikes.",
        "ChatGPT passes Turing Test in controlled academic evaluation.",
        "Massive coral bleaching event threatens Great Barrier Reef ecosystem.",
        "New malaria vaccine shows 80% efficacy in large African trial.",
        "EU proposes sweeping AI regulation laws, affecting global tech firms.",
        "ISRO successfully launches Gaganyaan crew module recovery test.",
        "Japan's population falls at record pace, prompting immigration policy shift.",
        "Google Gemini API now available to developers worldwide for free trials."
    ]



def ingest_articles():
    texts = fetch_reuters_articles()
    print(f"[*] Embedding {len(texts)} articles...")
    vectors = embedder.encode(texts).tolist()

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vectors[i],
            payload={"text": texts[i]}
        ) for i in range(len(texts))
    ]

    print(f"[*] Uploading to Qdrant ({len(points)} documents)...")
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    print("[+] Ingestion complete.")

if __name__ == "__main__":
    ingest_articles()
