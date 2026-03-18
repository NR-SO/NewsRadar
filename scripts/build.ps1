# Script de build para NEWSRADAR (PowerShell)

Write-Host "Iniciando build del proyecto NEWSRADAR..."

# Build de contenedores
Write-Host "Construyendo contenedores Docker..."
docker-compose build

Write-Host "Build completado exitosamente."
