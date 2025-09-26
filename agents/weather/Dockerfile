# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir \
    "a2a-sdk[http-server]==0.3.7" \
    "uvicorn==0.30.*" \
    "fastapi==0.115.*" \
    "httpx==0.27.*" \
    "mcp==1.15.*"

COPY src/ src/

EXPOSE 8082

CMD ["python", "-u", "src/a2a_server.py"]
