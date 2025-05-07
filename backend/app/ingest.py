import os
import uuid
import argparse
from dotenv import load_dotenv
import feedparser
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# Load environment variables
load_dotenv()

# Constants
COLLECTION_NAME = "news"
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

# Initialize Qdrant & Embedder
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_feeds():
    return [
        "https://www.theguardian.com/world/rss",
        "https://www.theguardian.com/international/rss",
        "https://www.theguardian.com/technology/rss",
        "https://www.theguardian.com/environment/rss",
        "https://hnrss.org/frontpage"
    ]

def fetch_rss_articles(limit: int) -> list[str]:
    print(f"[*] Fetching up to {limit} articles from RSS feeds...")
    articles = []
    for url in get_feeds():
        print(f"--> Fetching: {url}")
        feed = feedparser.parse(url)
        print(f"    ↪️ {len(feed.entries)} entries found")
        for entry in feed.entries:
            if len(articles) >= limit:
                break
            summary = entry.summary if hasattr(entry, "summary") else ""
            text = entry.title + ". " + summary
            articles.append(text)
        if len(articles) >= limit:
            break
    print(f"[*] Total RSS articles fetched: {len(articles)}")
    return articles

def fetch_mock_articles(limit: int) -> list[str]:
    data = [
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
    print(f"[*] Using mock dataset: {min(limit, len(data))} articles")
    return data[:limit]

def ingest_articles(source: str = "rss", limit: int = 30):
    if source == "rss":
        texts = fetch_rss_articles(limit)
        if not texts:
            print("⚠️ RSS failed. Falling back to mock data.")
            texts = fetch_mock_articles(limit)
    elif source == "mock":
        texts = fetch_mock_articles(limit)
    else:
        raise ValueError("Invalid source. Use 'rss' or 'mock'.")

    if not texts:
        print("❌ No articles to ingest. Exiting.")
        return

    print(f"[*] Embedding {len(texts)} articles...")
    vectors = embedder.encode(texts).tolist()

    # Create collection if not exists
    if COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vectors[i],
            payload={"text": texts[i]}
        ) for i in range(len(texts))
    ]

    print(f"[*] Uploading {len(points)} vectors to Qdrant...")
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    print("[+] Ingestion complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["rss", "mock"], default="rss", help="Choose data source")
    parser.add_argument("--limit", type=int, default=30, help="Number of articles to ingest")
    args = parser.parse_args()

    ingest_articles(source=args.source, limit=args.limit)
