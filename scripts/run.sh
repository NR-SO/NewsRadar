#!/bin/bash

# Script principal para ejecutar NEWSRADAR
# Este es el "comando único" del proyecto

set -e

echo "=========================================="
echo "NEWSRADAR - Ejecutando aplicación"
echo "=========================================="
echo ""

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi

echo "✓ Docker y Docker Compose disponibles"
echo ""

# Crear archivo .env si no existe
if [ ! -f config/.env.local ]; then
    echo "📋 Creando archivo de configuración .env.local..."
    cp config/.env.example config/.env.local
    echo "⚠️  Edita config/.env.local si necesitas cambiar valores"
else
    echo "✓ Archivo .env.local ya existe"
fi

echo ""
echo "🐳 Levantando servicios con Docker Compose..."
echo ""

# Build y levanta los servicios
docker-compose up -d --build

echo ""
echo "⏳ Esperando que los servicios estén listos..."
sleep 5

echo ""
echo "📊 Estado de los servicios:"
docker-compose ps

echo ""
echo "=========================================="
echo "✅ NEWSRADAR está en ejecución"
echo "=========================================="
echo ""
echo "Acceso a los servicios:"
echo "  🌐 Frontend: http://localhost:3000"
echo "  📡 API: http://localhost:8000"
echo "  📖 Docs API: http://localhost:8000/docs"
echo "  🗄️  MongoDB: localhost:27017"
echo ""
echo "Para ver logs:"
echo "  docker-compose logs -f"
echo ""
echo "Para detener:"
echo "  docker-compose down"
echo ""
