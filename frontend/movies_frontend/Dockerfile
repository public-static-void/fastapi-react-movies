# Stage 1: Builder
FROM node:22.9.0-alpine AS builder

ARG VITE_BACKEND
ENV VITE_BACKEND=$VITE_BACKEND

WORKDIR /app

# 1. Install pnpm
RUN npm install -g pnpm@10.9.0

# 2. Copy package files separately for better layer caching
COPY package.json pnpm-lock.yaml ./

# 3. Improved cache configuration with named mounts
RUN --mount=type=cache,id=pnpm_store,target=/root/.local/share/pnpm/store \
  --mount=type=cache,id=build_cache,target=/app/node_modules/.cache \
  pnpm install --frozen-lockfile --prefer-offline

# 4. Copy remaining files
COPY . .

# 5. Build with separate Vite cache and increased timeout
RUN --mount=type=cache,id=build_cache,target=/app/node_modules/.cache \
  --mount=type=cache,id=vite_cache,target=/app/node_modules/.vite \
  timeout 600 pnpm build --mode production || \
  (echo "Build timed out!" && exit 1)

# Stage 2: Production
FROM nginx:1.25.3-alpine-slim

# 6. Clean nginx root more efficiently
RUN find /usr/share/nginx/html -mindepth 1 -delete

# 7. Copy built assets and config
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
