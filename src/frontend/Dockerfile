# Dockerfile para NEWSRADAR Frontend (React)
# Multi-stage para optimizar tamaño

FROM node:18-alpine as builder

WORKDIR /build
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY --from=builder /build/build ./build
COPY --from=builder /build/public ./public

EXPOSE 3000

CMD ["npm", "start"]
