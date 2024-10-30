FROM node:22.9.0-alpine AS builder

ARG VITE_BACKEND
ENV VITE_BACKEND=$VITE_BACKEND

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install --production

COPY . .

RUN yarn build

FROM nginx:stable-alpine

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*

COPY --from=builder /app/dist .

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
