# Stage 1: Builder
FROM python:3.12-alpine AS builder

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
  build-base \
  libffi-dev \
  openssl-dev \
  postgresql-dev

WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements with cache
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
  pip install --no-cache-dir -r requirements.txt && \
  apk del .build-deps

# Stage 2: Runtime
FROM python:3.12-alpine

# Runtime dependencies
RUN apk add --no-cache libpq

WORKDIR /app

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=nobody:nobody . .

# Create unprivileged user
RUN adduser -D -u 1000 appuser && \
  chown -R appuser:appuser /app

USER appuser

ENV MM_DB_PATH=/tmp/db \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random

EXPOSE 8000
CMD ["python", "-m", "movies_backend.main"]
