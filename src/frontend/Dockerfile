# Dockerfile para NEWSRADAR Frontend (React)
# Multi-stage para optimizar tamaño y seguridad

FROM node:18-alpine AS builder

WORKDIR /build

# Actualizar paquetes del sistema y npm a versión 9+ para mejor resolución
RUN apk update && apk upgrade --no-cache && npm install -g npm@9

COPY package*.json ./

# Instalar dependencias de forma natural (requiere typescript 4.9.5 en package.json)
RUN npm install

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

# Actualizar paquetes del sistema
RUN apk update && apk upgrade --no-cache && npm install -g npm@9

COPY package*.json ./

# Instalar dependencias de producción de forma limpia
RUN npm install --omit=dev

COPY --from=builder /build/build ./build
COPY --from=builder /build/public ./public

EXPOSE 3000

CMD ["npm", "start"]