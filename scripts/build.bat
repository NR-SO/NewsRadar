@echo off
REM Script de build para NEWSRADAR

setlocal enabledelayedexpansion

echo Iniciando build del proyecto NEWSRADAR...

REM Build de contenedores
echo Construyendo contenedores Docker...
docker-compose build

echo Build completado exitosamente.
