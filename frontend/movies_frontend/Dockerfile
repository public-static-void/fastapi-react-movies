# Stage 1: Builder
FROM node:22.9.0-alpine AS builder

ARG VITE_BACKEND
ENV VITE_BACKEND=$VITE_BACKEND

WORKDIR /app

# Install pnpm with version pinning
RUN npm install -g pnpm@10.9.0

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies with cache
RUN --mount=type=cache,target=/root/.pnpm-store \
  --mount=type=cache,target=/app/node_modules/.cache \
  pnpm install --frozen-lockfile --prefer-offline

# Copy application code
COPY . .

# Build production assets with timeout
RUN timeout 300 pnpm build --mode production || \
  (echo "Build timed out!" && exit 1)

# Stage 2: Production
FROM nginx:1.25.3-alpine-slim

# Remove default content
RUN rm -rf /usr/share/nginx/html/*

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy Nginx config with health check
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
