FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable BuildKit cache mount for uv downloads
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r pyproject.toml

COPY src/ ./src/

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
