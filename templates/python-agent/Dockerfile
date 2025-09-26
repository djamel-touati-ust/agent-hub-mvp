FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --only main

COPY src /app/src

EXPOSE 8080
CMD ["python", "src/a2a_server.py"]
