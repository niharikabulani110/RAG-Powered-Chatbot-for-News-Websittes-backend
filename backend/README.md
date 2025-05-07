# News RAG API

A FastAPI-based backend service that implements a Retrieval-Augmented Generation (RAG) pipeline for news articles. This service allows users to query news content using natural language and get AI-generated responses based on relevant news articles.

## Features

- FastAPI backend with async support
- Redis integration for caching and storage
- Qdrant vector database for semantic search
- RAG pipeline for intelligent query processing
- News article ingestion and embedding generation
- Health check endpoint
- Environment variable configuration

## Setup

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
- Update the variables in `.env` with your configuration

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

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

- The project uses FastAPI for the web framework
- Redis is used for caching and storage
- Qdrant is used as the vector database
- OpenAI's API is used for embeddings and text generation

## License

MIT 