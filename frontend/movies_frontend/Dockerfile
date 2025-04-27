# Stage 1: Builder
FROM node:22.9.0-alpine AS builder

ARG VITE_BACKEND
ENV VITE_BACKEND=$VITE_BACKEND

WORKDIR /app

# 1. Install pnpm
RUN npm install -g corepack@latest && \
  COREPACK_ENABLE_UNSAFE=true corepack use pnpm@10.9.0

# 2. Single COPY command for package files
COPY package.json pnpm-lock.yaml ./

# 3. Cache configuration improvements
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
  --mount=type=cache,target=/app/node_modules/.cache \
  pnpm install --frozen-lockfile --prefer-offline

# 4. Copy necessary files
COPY . .

# 5. Build with cache preservation
RUN --mount=type=cache,target=/app/node_modules/.cache \
  timeout 300 pnpm build --mode production || \
  (echo "Build timed out!" && exit 1)

# Stage 2: Production
FROM nginx:1.25.3-alpine-slim

RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
