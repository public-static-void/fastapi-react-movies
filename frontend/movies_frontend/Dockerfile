# Stage 1: Builder
FROM node:22.9.0-alpine AS builder

ARG VITE_BACKEND
ENV VITE_BACKEND=$VITE_BACKEND

WORKDIR /app

# Install pnpm directly with version pinning
RUN npm install -g pnpm@10.9.0

# Copy package management files
COPY package.json pnpm-lock.yaml ./

# Install dependencies with aggressive caching
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
  --mount=type=cache,target=node_modules/.cache \
  pnpm install --frozen-lockfile --prefer-offline

# Copy remaining files
COPY . .

# Build with production optimizations
RUN pnpm build --mode production

# Stage 2: Optimized Nginx
FROM nginx:1.25.3-alpine-slim

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Use custom Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Remove default Nginx configurations
RUN rm -rf /etc/nginx/conf.d/default.conf.bak

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
