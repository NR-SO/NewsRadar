# Script de deploy para NEWSRADAR (PowerShell)

Write-Host "Iniciando deploy del proyecto NEWSRADAR..."

# Pull de codigo
git pull origin main

# Build
. .\scripts\build.ps1

# Stop de contenedores actuales
docker-compose down

# Iniciar nuevos contenedores
docker-compose up -d

Write-Host "Deploy completado exitosamente."
