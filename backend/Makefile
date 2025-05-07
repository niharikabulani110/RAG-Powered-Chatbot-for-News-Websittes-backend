# Makefile for RAG-powered chatbot backend

# Services
DOCKER_COMPOSE = docker-compose
BACKEND_CONTAINER = rag-news-backend

# === Docker Commands ===

up:
	$(DOCKER_COMPOSE) up --build

down:
	$(DOCKER_COMPOSE) down

restart: down up

logs:
	$(DOCKER_COMPOSE) logs -f

# === Ingestion ===

ingest:
	docker-compose run --rm backend python app/ingest.py


# === Testing ===

chat:
	curl -X POST http://localhost:8000/chat \
		-H "accept: application/json" \
		-H "Content-Type: application/json" \
		-d '{"query": "What are the recent developments in the Israel-Palestine conflict?", "session_id": ""}'

# === Utilities ===

shell:
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) bash

health:
	curl -s http://localhost:8000/healthz

# === Housekeeping ===

clean:
	$(DOCKER_COMPOSE) down -v
	docker system prune -f
