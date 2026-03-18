# Script de test para NEWSRADAR (PowerShell)

Write-Host "Ejecutando test del proyecto NEWSRADAR..."

# Ejecutar pruebas
Write-Host "Ejecutando pruebas unitarias..."
python -m pytest tests/unit -v

Write-Host "Ejecutando pruebas funcionales..."
python -m pytest tests/functional -v

Write-Host "Test completado exitosamente."
