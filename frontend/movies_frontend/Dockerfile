FROM node:22.9.0-alpine AS builder

ARG VITE_BACKEND
ENV VITE_BACKEND=$VITE_BACKEND

WORKDIR /app

# Install pnpm directly (bypass Corepack issues)
RUN npm install -g pnpm@latest

# Copy ALL configuration files first
COPY package.json pnpm-lock.yaml ./
COPY tsconfig.json tsconfig.node.json ./
COPY vite.config.ts ./
COPY eslint.config.js ./

# Install dependencies with cache
RUN --mount=type=cache,target=/root/.pnpm-store \
  pnpm install --frozen-lockfile --prefer-offline

# Copy application code
COPY index.html index.html
COPY src ./src
COPY public ./public

# Build with error resilience
RUN pnpm build || (echo "Build failed, checking config..." && cat tsconfig.json && exit 1)

FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
