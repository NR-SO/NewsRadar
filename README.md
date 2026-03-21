# NEWSRADAR

**Proyecto Académico - Grado en Ingeniería Informática, UC3M**

Sistema de procesamiento y análisis de canales RSS con clasificación automática mediante IPTC Media Topics y visualización interactiva en tiempo real.

---

## Tabla de contenidos

- [Requisitos previos](#requisitos-previos)
- [Clonar el repositorio](#clonar-el-repositorio)
- [Ejecución rápida (1 Comando)](#ejecución-rápida-1-comando)
- [Build](#build)
- [Test](#test)
- [Deploy](#deploy)
- [Acceso a los servicios](#acceso-a-los-servicios)
- [Documentación](#documentación)

---

## Requisitos previos

- **Docker** y **Docker Compose** (v1.29+)
- **Git**

---

## Clonar el repositorio

```bash
git clone [https://github.com/EliiSD/NewsRadar.git](https://github.com/EliiSD/NewsRadar.git)
cd NewsRadar
```

---

## Ejecución rápida (1 Comando)

Este es el comando único que levanta toda la infraestructura de forma aislada (Base de datos, Backend, Frontend):

```bash
docker-compose up --build -d
```

Para monitorizar los logs en tiempo real:
```bash
docker-compose logs -f
```

Para ver logs de un servicio específico:

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

---

## Build

Para reconstruir las imágenes Docker desde cero (por ejemplo, si añades nuevas dependencias al `package.json` o `requirements.txt`):

```bash
docker-compose build --no-cache
```

---

## Test

Las pruebas se ejecutan directamente dentro de los contenedores Docker para garantizar la reproducibilidad del entorno:

**Pruebas unitarias del backend (FastAPI):**
```bash
docker exec -it newsradar-backend pytest -v
```

**Pruebas del frontend (React):**
```bash
docker exec -it newsradar-frontend npm test -- --watchAll=false
```

---

## Deploy

El sistema está contenerizado y listo para su despliegue en entornos de producción. 

Para reiniciar el entorno completo:
```bash
docker-compose down && docker-compose up -d
```

Para detener y limpiar la infraestructura completa (CUIDADO: borra los volúmenes de base de datos):
```bash
docker-compose down -v
```

---

## Acceso a los servicios

Una vez levantada la aplicación, los servicios estarán disponibles en los siguientes endpoints:

| Servicio | URL | Puerto Interno |
|----------|-----|----------------|
| **Frontend (React)** | http://localhost:3000 | 3000 |
| **API Backend (FastAPI)** | http://localhost:8000 | 8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs | - |
| **API Docs (ReDoc)** | http://localhost:8000/redoc | - |
| **Base de Datos (MongoDB)** | mongodb://localhost:27017 | 27017 |

---

## Documentación

- [Architecture Decision Records (ADR)](docs/adr/README.md) - Decisiones arquitectónicas.
- [Especificación técnica](docs/requirements/especificacion.md) - Requisitos técnicos detallados.
- [Registro de prompts IA](docs/prompts_ia.md) - Trazabilidad del uso de IA en el proyecto.

---

## Estructura del proyecto

```text
NewsRadar/
├── src/
│   ├── backend/             # API REST en FastAPI
│   │   ├── app/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── frontend/            # Interfaz en React.js
│       ├── public/
│       ├── src/
│       ├── package.json
│       └── Dockerfile
├── docs/
│   ├── adr/                  # Architecture Decision Records
│   ├── requirements/         # Especificaciones
│   └── prompts_ia.md
├── scripts/
│   ├── run.sh               # Script principal para ejecutar
│   ├── test.sh              # Script de tests
│   ├── build.sh
│   └── deploy.sh
├── tests/
│   ├── unit/                # Pruebas unitarias
│   └── functional/          # Pruebas funcionales
├── config/
│   └── .env.example
├── data/
│   ├── seed.json
│   └── init-mongo.js
└── docker-compose.yml       # Orquestación de servicios
```

---

## Contribución

Por favor, siga las siguientes convenciones:
1. Cree una rama para cada feature: `git checkout -b feature/descripcion`
2. Haga commits descriptivos.
3. Envíe un pull request detallando los cambios.

## Licencia

Proyecto académico - UC3M, 2026

## Contacto

Para dudas o sugerencias, contacte al equipo de desarrollo.
**Versión:** 1.0 - Sprint 1