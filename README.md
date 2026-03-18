# NEWSRADAR 📡

**Proyecto Académico - Grado en Ingeniería Informática, UC3M**

Sistema de procesamiento y análisis de canales RSS con clasificación automática mediante IPTC Media Topics y visualización interactiva en tiempo real.

---

## 📋 Tabla de contenidos

- [Requisitos previos](#requisitos-previos)
- [Clonar el repositorio](#clonar-el-repositorio)
- [Comando único para ejecutar todo](#comando-único-para-ejecutar-todo)
- [Build](#build)
- [Test](#test)
- [Deploy](#deploy)
- [Acceso a los servicios](#acceso-a-los-servicios)
- [Documentación](#documentación)

---

## 🔧 Requisitos previos

- **Docker** y **Docker Compose** (v1.29+)
- **Git**
- **Python** 3.11+ (solo para desarrollo local sin Docker)
- **Node.js** 18+ (solo para desarrollo local sin Docker)

---

## 🚀 Clonar el repositorio

```bash
git clone https://github.com/EliiSD/NewsRadar.git
cd NewsRadar
```

---

## ⚡ Comando único para ejecutar todo

Este es el comando que levanta toda la infraestructura (Base de datos, Backend, Frontend):

```bash
docker-compose up -d
```

Para ver los logs de todos los servicios:

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

## 🏗️ Build

### Build con Docker (recomendado)

```bash
docker-compose build
```

Este comando reconstruye todas las imágenes Docker desde cero.

### Build manual (sin Docker)

**Backend:**
```bash
cd src/backend
pip install -r requirements.txt
cd ../..
```

**Frontend:**
```bash
cd src/frontend
npm install
cd ../..
```

---

## 🧪 Test

### Ejecutar tests con script automatizado

```bash
bash scripts/test.sh
```

### Ejecutar tests manualmente

**Pruebas unitarias del backend:**
```bash
python -m pytest tests/unit -v
```

**Pruebas funcionales:**
```bash
python -m pytest tests/functional -v
```

**Pruebas de salud de la API:**
```bash
python -m pytest tests/unit/test_health.py -v
```

**Todas las pruebas con cobertura:**
```bash
python -m pytest tests/ -v --cov=src/backend --cov-report=html
```

---

## 🚢 Deploy

### Deploy con Docker Compose (desarrollo/preproducción)

```bash
bash scripts/run.sh
```

O manualmente:

```bash
docker-compose up -d --build
```

Esperar a que todos los servicios estén healthy:

```bash
docker-compose ps
```

### Detener la aplicación

```bash
docker-compose down
```

Detener y eliminar volúmenes (cuidado: borra datos):

```bash
docker-compose down -v
```

---

## 🌐 Acceso a los servicios

Una vez levantada la aplicación:

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **Frontend** | http://localhost:3000 | - |
| **API Backend** | http://localhost:8000 | - |
| **API Docs (Swagger)** | http://localhost:8000/docs | - |
| **API Docs (ReDoc)** | http://localhost:8000/redoc | - |
| **PostgreSQL** | localhost:5432 | user: `newsradar`, password: `newsradar` |
| **pgAdmin** | http://localhost:5050 | user: `admin@newsradar.local`, password: `admin` |

---

## 📚 Documentación

### Documentación del proyecto

- [Architecture Decision Records](docs/adr/README.md) - Decisiones arquitectónicas
- [Especificación técnica](docs/requirements/especificacion.md) - Requisitos técnicos detallados
- [Prompts IA utilizados](docs/prompts_ia.md) - Registro de prompts para la IA

---

## 📁 Estructura del proyecto

```
NewsRadar/
├── src/
│   ├── backend/              # FastAPI application
│   │   ├── app/
│   │   ├── main.py           # Punto de entrada
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── frontend/             # React application
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
│   ├── .env.example
│   ├── dockerfile.backend
│   ├── dockerfile.frontend
│   └── nginx.conf
├── data/
│   ├── seed.json
│   └── init-mongo.js
└── docker-compose.yml       # Orquestación de servicios
```

---

## 🐛 Troubleshooting

### Los servicios no responden

Verificar que están corriendo:
```bash
docker-compose ps
```

### Ver logs de errores

```bash
docker-compose logs backend
```

### Reiniciar los servicios

```bash
docker-compose restart
```

### Problemas con puertos ocupados

Si los puertos 3000, 8000, 5432 están ocupados, editar `docker-compose.yml` y cambiar los puertos.

---

## 📄 Licencia

Proyecto académico - UC3M, 2026

---

## 👥 Contacto

Para preguntas sobre este proyecto, contactar al equipo de desarrollo.

**Última actualización:** Marzo 2026  
**Versión:** 1.0 - Sprint 1

## Deploy

Para desplegar en producción:

# Configurar variables de entorno
cp config/.env.example config/.env.production
# Editar config/.env.production con valores correctos

# Ejecutar con compose en producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

## Estructura del proyecto

├── src/
│   ├── backend/         - API REST en FastAPI
│   └── frontend/        - Interfaz en React.js
├── docs/
│   ├── adr/             - Architecture Decision Records
│   └── requirements/    - Especificaciones de requisitos
├── scripts/             - Scripts de automatización
├── tests/
│   ├── unit/            - Pruebas unitarias
│   └── functional/      - Pruebas funcionales
├── config/              - Configuración y variables de entorno
├── data/                - Datos de prueba
├── .github/workflows/   - Pipeline CI/CD
└── docker-compose.yml   - Orquestacion de contenedores

## Documentacion

- [Architecture Decision Records](docs/adr/README.md)
- [Requisitos del Sistema](docs/requirements/README.md)

## Contribucion

Por favor, siga las siguientes convenciones:
- Cree una rama para cada feature: \git checkout -b feature/descripcion\
- Haga commits descriptivos
- Envíe un pull request con descripción detallada

## Licencia

Se utilizará la licencia especificada en LICENSE.

## Contacto

Para dudas o sugerencias, contacte al equipo de desarrollo.
