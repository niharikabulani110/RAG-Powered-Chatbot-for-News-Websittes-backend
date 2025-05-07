# News RAG API

A FastAPI-based backend service that implements a Retrieval-Augmented Generation (RAG) pipeline for news articles. This service allows users to query news content using natural language and get AI-generated responses based on relevant news articles.

## Features

- 📰 News article ingestion from RSS feeds with fallback to mock data
- 🔍 Semantic search using SentenceTransformer embeddings
- 🤖 AI-powered responses using Google's Gemini API
- 💾 Vector storage with Qdrant
- 🔄 Session management with Redis
- 🗄️ PostgreSQL database for transcript storage
- 🐳 Docker and Docker Compose support
- 🚀 FastAPI backend with async support
- 🔒 CORS-enabled for frontend integration
- 📊 Health check endpoint
- ⚙️ Environment variable configuration

## Architecture

### RAG Pipeline Flow
1. **Data Ingestion**
   - RSS feed scraping from multiple news sources (The Guardian, Hacker News)
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

### Data Storage
- **Vector Database (Qdrant)**
  - Stores article embeddings and text
  - Enables semantic search
  - Persistent storage with Docker volumes

- **Session Management (Redis)**
  - UUID-based session identification
  - Redis-based chat history storage
  - Session expiry after 24 hours (configurable)
  - Automatic session cleanup

- **Transcript Storage (PostgreSQL)**
  - Stores all chat transcripts
  - Includes session ID, user input, bot response, and timestamp
  - Persistent storage with Docker volumes

## Setup

### Prerequisites
- Docker and Docker Compose
- Google Gemini API key

### Installation

1. Clone the repository and navigate to the backend directory:
```bash
cd backend
```

2. Configure environment variables:
- Create a `.env` file with the following variables:
  ```plaintext
  GEMINI_API_KEY=your_gemini_api_key
  REDIS_HOST=redis
  REDIS_PORT=6379
  QDRANT_HOST=qdrant
  QDRANT_PORT=6333
  QDRANT_URL=http://qdrant:6333
  DATABASE_URL=postgresql://verifast:verifast123@db:5432/chatbot
  ```

3. Start the services using Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Manual Setup (without Docker)

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the required services:
```bash
# Start PostgreSQL
docker run -d --name postgres \
  -e POSTGRES_USER=verifast \
  -e POSTGRES_PASSWORD=verifast123 \
  -e POSTGRES_DB=chatbot \
  -p 5432:5432 \
  postgres:15

# Start Redis
docker run -d --name redis -p 6380:6379 redis:alpine

# Start Qdrant
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

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

## Data Management

### Redis Configuration
- TTL: 24 hours (configurable)
- Storage: List data structure
- Format: Alternating Q&A pairs
- Example:
  ```
  session_id -> ["User: question1", "Bot: answer1", "User: question2", "Bot: answer2"]
  ```

### PostgreSQL Schema
```sql
CREATE TABLE transcripts (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR,
    user_input TEXT,
    bot_response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Project Structure

```
backend/
├── app/
│   ├── main.py            # FastAPI entrypoint
│   ├── rag.py             # RAG pipeline implementation
│   ├── redis_client.py    # Redis client configuration
│   ├── db.py             # PostgreSQL database models
│   ├── ingest.py         # News scraping and embedding generation
│   └── models.py         # Pydantic models
├── requirements.txt      # Project dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── .env                # Environment variables
```

## Development

### Technologies Used
- FastAPI for the web framework
- Redis for session management
- Qdrant for vector database
- PostgreSQL for transcript storage
- Google Gemini API for text generation
- SentenceTransformers for embeddings
- Docker for containerization

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