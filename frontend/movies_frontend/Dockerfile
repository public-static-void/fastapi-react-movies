FROM node:22.9.0-slim AS builder

ARG VITE_BACKEND
ENV VITE_BACKEND=$VITE_BACKEND

WORKDIR /app

COPY package*.json ./

RUN npm install --omit=dev

COPY . .

RUN npm run build

FROM nginx:stable-alpine

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*

COPY --from=builder /app/dist .

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
