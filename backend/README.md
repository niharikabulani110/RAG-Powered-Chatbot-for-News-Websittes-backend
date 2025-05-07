# News RAG API

A FastAPI-based backend service that implements a Retrieval-Augmented Generation (RAG) pipeline for news articles. This service allows users to query news content using natural language and get AI-generated responses based on relevant news articles.

## Features

- 📰 News article ingestion from RSS feeds with fallback to mock data
- 🔍 Semantic search using SentenceTransformer embeddings
- 🤖 AI-powered responses using Google's Gemini API
- 💾 Vector storage with Qdrant
- 🔄 Session management with Redis
- 🚀 FastAPI backend with async support
- 🔒 CORS-enabled for frontend integration
- 📊 Health check endpoint
- ⚙️ Environment variable configuration

## Architecture

### RAG Pipeline Flow
1. **Data Ingestion**
   - RSS feed scraping from multiple news sources
   - Fallback to mock data if RSS fails
   - Text preprocessing and cleaning

2. **Embedding Generation**
   - Uses SentenceTransformer's "all-MiniLM-L6-v2" model
   - Generates 384-dimensional embeddings
   - Cosine similarity for semantic search

3. **Vector Storage**
   - Qdrant vector database for efficient similarity search
   - Stores article text and corresponding embeddings
   - Configurable collection parameters

4. **Query Processing**
   - User query embedding generation
   - Top-k document retrieval (k=3)
   - Context-aware response generation using Gemini API

### Session Management
- UUID-based session identification
- Redis-based chat history storage
- Session expiry after 1 hour (configurable)
- Automatic session cleanup

## Setup

### Prerequisites
- Python 3.8+
- Redis server
- Qdrant server
- Google Gemini API key

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the variables in `.env` with your configuration:
  ```plaintext
  GEMINI_API_KEY=your_gemini_api_key
  REDIS_HOST=localhost
  REDIS_PORT=6379
  QDRANT_HOST=localhost
  QDRANT_PORT=6333
  ```

4. Start the services:
```bash
# Start Redis (if not running)
redis-server

# Start Qdrant (if not running)
docker run -p 6333:6333 qdrant/qdrant

# Run the application
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

### Available Endpoints

#### Chat Endpoints
- `POST /chat`
  - Accepts user message
  - Returns AI-generated response
  - Request body: `{"query": "your question", "session_id": "optional-uuid"}`

#### Session Management
- `GET /history/{session_id}`
  - Returns chat history for the session
- `POST /reset/{session_id}`
  - Clears chat history for the session

## Redis Configuration

### Session Management
- TTL: 1 hour (configurable)
- Storage: List data structure
- Format: Alternating Q&A pairs
- Example:
  ```
  session_id -> ["Q: question1", "A: answer1", "Q: question2", "A: answer2"]
  ```

### TTL Configuration
```python
# Example Redis TTL configuration
REDIS_SESSION_TTL = 3600  # 1 hour in seconds
REDIS_MAX_SESSIONS = 1000  # Maximum concurrent sessions
```

## Project Structure

```
backend/
├── app/
│   ├── main.py            # FastAPI entrypoint
│   ├── rag.py             # RAG pipeline implementation
│   ├── redis_client.py    # Redis client configuration
│   ├── ingest.py          # News scraping and embedding generation
│   └── models.py          # Pydantic models
├── requirements.txt       # Project dependencies
└── .env                  # Environment variables
```

## Development

### Technologies Used
- FastAPI for the web framework
- Redis for caching and storage
- Qdrant for vector database
- Google Gemini API for text generation
- SentenceTransformers for embeddings

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 