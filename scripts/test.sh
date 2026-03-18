#!/bin/bash

# Script de testing para NEWSRADAR
# Ejecuta toda la suite de tests

set -e

echo "=========================================="
echo "NEWSRADAR - Testing"
echo "=========================================="
echo ""

# Verificar que pytest está instalado
if ! command -v pytest &> /dev/null; then
    echo "⚠️  pytest no está instalado, instalando dependencias..."
    cd src/backend
    pip install -r requirements-dev.txt
    cd ../..
fi

echo "🧪 Ejecutando suite de tests..."
echo ""

# Ejecutar tests unitarios
echo "📋 Pruebas unitarias..."
python -m pytest tests/unit/test_health.py -v --tb=short

echo ""
echo "📋 Todas las pruebas..."
python -m pytest tests/ -v --tb=short --cov=src/backend --cov-report=term-missing

echo ""
echo "=========================================="
echo "✅ Testing completado"
echo "=========================================="
echo ""
