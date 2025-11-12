# syntax=docker/dockerfile:1.4
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_NO_CACHE=1

WORKDIR /app

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        curl ca-certificates build-essential \
    ; rm -rf /var/lib/apt/lists/*

RUN mkdir -p "$TMPDIR"

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# ------- deps layer (cacheable) ---------
COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache uv sync --frozen --no-dev
# RUN uv sync --frozen --no-dev

ENV PATH="app/.venv/bin:${PATH}"

# --- app layer ---
COPY . .

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=5 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "server.address=0.0.0.0", "--server.headless=true"]
