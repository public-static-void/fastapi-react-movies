# Stage 1: Builder
FROM python:3.12-alpine AS builder

RUN apk add --no-cache --virtual .build-deps \
  build-base \
  libffi-dev \
  openssl-dev \
  postgresql-dev

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend/movies_backend/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
  pip install --no-cache-dir -r requirements.txt && \
  apk del .build-deps

# Stage 2: Runtime
FROM python:3.12-alpine

RUN apk add --no-cache libpq

WORKDIR /app

# Create db directory
RUN mkdir -p db

# Copy the entire db folder into the container
RUN mkdir -p /var/db/movies_backend
COPY backend/db /var/db/movies_backend

# Create appuser
RUN adduser -D -u 1000 appuser

# Copy venv and app code as root
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY backend/movies_backend /app/movies_backend
COPY backend/db /var/db/movies_backend

# Set ownership to appuser
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000
CMD ["python", "-m", "movies_backend.main"]
