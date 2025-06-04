FROM python:3.12.6-alpine

# Essential build dependencies
RUN apk add --no-cache --virtual .build-deps \
  build-base libffi-dev openssl-dev postgresql-dev && \
  pip install -r requirements.txt && \
  apk del .build-deps

WORKDIR /app

# Install requirements first for caching
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
  pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Security context
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["python", "-m", "movies_backend.main"]
