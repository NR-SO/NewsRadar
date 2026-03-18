@echo off
REM Script de test para NEWSRADAR

setlocal enabledelayedexpansion

echo Ejecutando test del proyecto NEWSRADAR...

REM Ejecutar pruebas
echo Ejecutando pruebas unitarias...
python -m pytest tests/unit -v

echo Ejecutando pruebas funcionales...
python -m pytest tests/functional -v

echo Test completado exitosamente.
