@echo off
REM Script de deploy para NEWSRADAR

setlocal enabledelayedexpansion

echo Iniciando deploy del proyecto NEWSRADAR...

REM Pull de codigo
git pull origin main

REM Build
call scripts/build.bat

REM Stop de contenedores actuales
docker-compose down

REM Iniciar nuevos contenedores
docker-compose up -d

echo Deploy completado exitosamente.
