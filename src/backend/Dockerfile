# Dockerfile para NEWSRADAR Backend (FastAPI)
# Multi-stage para optimizar tamaño y seguridad

FROM python:3.11-slim AS builder

WORKDIR /build

# Actualizar paquetes base y dependencias de compilacion
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# ELIMINADO --no-deps para empaquetar todo el arbol de dependencias
RUN pip wheel --no-cache-dir --wheel-dir /opt/wheels -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

# Actualizar paquetes del sistema en la imagen final
RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/wheels /opt/wheels
COPY requirements.txt .

RUN pip install --no-cache-dir --no-index --find-links=/opt/wheels -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]