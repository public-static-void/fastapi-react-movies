# Stage 1: Builder
FROM python:3.12-alpine AS builder

RUN apk add --no-cache --virtual .build-deps \
  build-base \
  libffi-dev \
  openssl-dev \
  postgresql-dev

WORKDIR /app

# Toolchain installs to system python, deliberately before the venv
# exists: the venv is what ships to the runtime stage, so poetry must
# not end up inside it.
RUN pip install --no-cache-dir poetry==2.2.1 poetry-plugin-export==1.10.1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend/movies_backend/pyproject.toml backend/movies_backend/poetry.lock backend/movies_backend/README.md ./
RUN poetry check --lock
RUN tmp="$(mktemp)" && \
  poetry export -f requirements.txt --output "$tmp" --only main && \
  pip install --no-cache-dir -r "$tmp" && \
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
COPY backend/movies_backend/movies_backend /app/movies_backend
COPY backend/db /var/db/movies_backend

# Set ownership to appuser
RUN chown -R appuser:appuser /app
RUN mkdir -p /var/db/movies_backend && chown -R appuser:appuser /var/db/movies_backend

USER appuser

EXPOSE 8000
CMD ["python", "-m", "movies_backend.main"]
