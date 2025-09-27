# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Upgrade pip tooling first
RUN python -m pip install --upgrade pip setuptools wheel

# Install each dependency individually (easy to see which one fails)
RUN pip install --prefer-binary 'a2a-sdk[http-server]==0.3.7'
RUN pip install 'uvicorn==0.34.3'
RUN pip install 'fastapi==0.115.14'
RUN pip install 'httpx==0.27.2'
RUN pip install 'mcp==1.15.0'

# Copy source last
COPY src/ /app/src/

# Calculator A2A listens on 8081
EXPOSE 8081

# Default to A2A server (override CMD if you need MCP in a container)
CMD ["python", "-m", "src.a2a_server"]
