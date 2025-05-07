# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system-level dependencies (optional, e.g., for feedparser or SSL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY ./app ./app

# Set PYTHONPATH so FastAPI can find modules
ENV PYTHONPATH=/app

# Run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
