# Stage 1: Builder
FROM node:22.9.0-alpine AS builder

ARG VITE_BACKEND
ENV VITE_BACKEND=$VITE_BACKEND

WORKDIR /app

# 1. Copy package files separately for better layer caching
COPY package.json package-lock.json ./

# 2. Install dependencies
RUN npm ci

# 3. Copy remaining files
COPY . .

# 4. Build with low memory usage
ENV NODE_ENV=production
RUN NODE_OPTIONS="--max-old-space-size=448" npm run build

# Stage 2: Production
FROM nginx:1.25.3-alpine-slim

# 5. Clean nginx root more efficiently
RUN find /usr/share/nginx/html -mindepth 1 -delete

# 6. Copy built assets and config
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
