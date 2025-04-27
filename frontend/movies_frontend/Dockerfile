# Stage 1: Builder
FROM node:22.9.0-alpine AS builder

ARG VITE_BACKEND
ENV VITE_BACKEND=$VITE_BACKEND

WORKDIR /app

# Install pnpm with version pinning
RUN npm install -g pnpm@10.9.0

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies with corrected cache syntax
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
  --mount=type=cache,target=/app/node_modules/.cache \
  pnpm install --frozen-lockfile --prefer-offline

COPY . .

# Build production assets
RUN pnpm build --mode production

# Stage 2: Production
FROM nginx:1.25.3-alpine-slim

# Remove default content
RUN rm -rf /usr/share/nginx/html/*

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
