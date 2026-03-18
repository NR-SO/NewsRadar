# Prompts de IA Utilizados - NEWSRADAR

**Objetivo:** Registro de los prompts utilizados en la generación automatizada del proyecto, como requisito académico.

**Versión:** 1.0  
**Última actualización:** Marzo 2026

---

## 1. Prompt Inicial - Estructura del Proyecto

### Fecha: Marzo 18, 2026

**Contexto:** Inicio del Sprint 1

**Prompt Original:**

```
Actúa como un experto en Ingeniería de Software. Necesito generar la estructura 
de directorios inicial para el proyecto académico NEWSRADAR (Grado en Ingeniería 
Informática, UC3M). La estructura debe seguir estrictamente estos requisitos:

/src: Para el código fuente (backend FastAPI y frontend React/D3.js).
/docs: Para documentación en Markdown, incluyendo una subcarpeta /docs/adr 
para Architecture Decision Records y /docs/requirements para especificaciones.
/scripts: Scripts de bash/python para build, test, run y deploy 
(fundamentales para el examen).
/tests: Carpetas para pruebas unitarias y funcionales.
/config: Archivos de configuración de entorno, Docker y dependencias.
/data: Datos iniciales (ej. JSON con los canales RSS iniciales e IPTC Media Topics).

Raíz: Un archivo README.md que incluya las secciones: Instalación, Build, Test y Deploy.

Por favor, genera un script de terminal (bash) que cree todas estas carpetas 
y archivos vacíos (usando touch para los archivos clave como .env.example, 
docker-compose.yml, requirements.txt y main.py en src). El objetivo es cumplir 
con el Sprint 1: Base técnica y repositorio.
```

**Resultado:** ✅ Script `init_structure.sh` y estructura de carpetas generada

---

## 2. Prompt - Dockerfiles y Configuración

### Fecha: Marzo 18, 2026

**Contexto:** Necesidad de generar Dockerfiles optimizados

**Prompt Original:**

```
Crea dos Dockerfiles multi-stage optimizados:

1. Backend (FastAPI):
   - Usar Python 3.11-slim
   - Multi-stage: builder + runtime
   - Instalar dependencias de requirements.txt
   - Exponer puerto 8000
   - Health check incluido

2. Frontend (React + D3.js):
   - Usar Node 18-alpine como builder
   - Build de producción React
   - Servir desde Nginx o node-server
   - Exponer puerto 3000

Además:
- Crear docker-compose.yml con servicios: backend, frontend
- Incluir red Docker compartida
- Incluir health checks
- Variables de entorno
```

**Resultado:** ✅ Dockerfiles profesionales creados en `/config` y `/src`

---

## 3. Prompt - MongoDB y Estructura Completa

### Fecha: Marzo 18, 2026

**Contexto:** Requisito de usar MongoDB según enunciado académico

**Prompt Original:**

```
Actualiza el docker-compose.yml para incluir:

1. Servicio MongoDB 7.0:
   - Usuario root: admin
   - Password configurable
   - Volumen persistente: mongodb_data
   - Health check

2. Backend FastAPI:
   - Conexión a MongoDB MONGODB_URL
   - Depends on MongoDB con service_healthy
   - Reload enabled para desarrollo

3. Frontend React:
   - REACT_APP_API_URL apuntando a backend
   - Volumen de código para desarrollo

Asegura que esté todo documentado en el README.
```

**Resultado:** ✅ Docker compose actualizado con MongoDB

---

## 4. Prompt - Especificación Técnica Completa

### Fecha: Marzo 18, 2026

**Contexto:** Documentación de requisitos según PDF del proyecto

**Prompt Original:**

```
Crea un documento de especificación técnica (especificacion.md) que incluya:

1. Requisitos Funcionales (RF-001 a RF-005):
   - Agregar fuentes RSS
   - Procesar feeds
   - Clasificación IPTC
   - Visualización
   - Alertas y notificaciones

2. Requisitos No Funcionales:
   - Rendimiento (Lighthouse > 80)
   - Escalabilidad (1M+ artículos)
   - Disponibilidad (99.5% uptime)
   - Seguridad (JWT, validación)
   - Mantenibilidad (70% test coverage)

3. Modelos de datos MongoDB:
   - Colección sources
   - Colección articles
   - Colección users

4. Endpoints API para Sprint 1 y futuros

5. Cronograma (5 sprints de 2 semanas)

6. Estrategia de testing
```

**Resultado:** ✅ Documento especificacion.md completo de 300+ líneas

---

## 5. Prompt - ADR sobre Decisiones Arquitectónicas

### Fecha: Marzo 18, 2026

**Contexto:** Justificación de tecnologías elegidas

**Prompt Original:**

```
Crea un Architecture Decision Record (ADR-0001) justificando las siguientes 
decisiones de tecnología:

1. FastAPI + Python para backend (vs Node.js, Spring Boot)
2. MongoDB para base de datos (vs PostgreSQL, Redis)
3. React + D3.js para frontend (vs Angular, Vue, Svelte)
4. Docker + Docker Compose para contenedores
5. GitHub Actions para CI/CD

Para cada decisión:
- Problema / contexto
- Decisión tomada
- Rationale detallado
- Alternativas consideradas y rechazadas
- Consecuencias (positivas y riesgos)
- Referencias

Usa markdown format profesional de ADR.
```

**Resultado:** ✅ ADR-0001-arquitectura-base.md con decisiones justificadas

---

## 6. Prompt - Tests Unitarios

### Fecha: Marzo 18, 2026

**Contexto:** Validación de pipeline CI/CD

**Prompt Original:**

```
Crea un archivo test_health.py con:

1. Fixture de TestClient para FastAPI
2. Test class: TestHealthEndpoint
   - Verifica que GET /health devuelve 200
   - Verifica estructura JSON (status, service, version)
   - Verifica valores correctos
   - Verifica Content-Type: application/json

3. Test class: TestAPIDocumentation
   - Verifica que /docs (Swagger) está disponible
   - Verifica que /redoc está disponible
   - Verifica que /openapi.json devuelve schema válido

Usa pytest con buenas prácticas:
- Funciones descriptivas
- Assertions claros
- Docstrings
- Fixture pattern
```

**Resultado:** ✅ test_health.py con cobertura completa del health check

---

## 7. Prompt - README Completo con Instrucciones

### Fecha: Marzo 18, 2026

**Contexto:** Requisito de README con instrucciones paso a paso

**Prompt Original:**

```
Actualiza el README.md para incluir:

1. Clonación del repositorio (comando git clone)
2. Comando ÚNICO para ejecutar todo (docker-compose up -d)
3. Instrucciones de Build (docker-compose build)
4. Instrucciones de Test (pytest, rutas)
5. Instrucciones de Deploy (scripts, docker-compose)
6. Tabla de acceso a servicios (puertos, URLs, credenciales)
7. Estructura del proyecto (tree)
8. Troubleshooting

Usa markdown profesional con:
- Emojis para claridad
- Tablas para información estructurada
- Bloques de código
- Links a documentación
```

**Resultado:** ✅ README.md de 300+ líneas con todas las secciones requeridas

---

## 8. Prompts Internos de Revisión

**Prompt de Revisión General:**

```
Revisa todo el repositorio para que se cumpla:
- README.md con instrucciones paso a paso
- docker-compose.yml con 3+ servicios
- .gitignore completo
- .github/workflows/ci.yml funcional
- /src/backend/main.py con /health endpoint
- /src/backend/requirements.txt
- /src/backend/Dockerfile
- /src/frontend/ estructura base
- /src/frontend/Dockerfile
- /docs/adr/0001-arquitectura-base.md
- /docs/requirements/especificacion.md
- /docs/prompts_ia.md
- /scripts/run.sh y test.sh
- /tests/unit/test_health.py
- /config/.env.example
- /data/seed.json
```

**Resultado:** ✅ Checklist de requisitos académicos completado

---

## Índice de Prompts

| # | Tema | Fecha | Estado |
|---|------|-------|--------|
| 1 | Estructura inicial | 2026-03-18 | ✅ Completado |
| 2 | Dockerfiles | 2026-03-18 | ✅ Completado |
| 3 | MongoDB integration | 2026-03-18 | ✅ Completado |
| 4 | Especificación técnica | 2026-03-18 | ✅ Completado |
| 5 | ADR arquitectura | 2026-03-18 | ✅ Completado |
| 6 | Tests unitarios | 2026-03-18 | ✅ Completado |
| 7 | README completo | 2026-03-18 | ✅ Completado |
| 8 | Revisión completa | 2026-03-18 | ⏳ En progreso |

---

## Notas sobre Generación Automática

**Observaciones importantes:**

1. **Iteraciones:** Cada componente requirió 1-2 iteraciones de refinamiento
2. **Validación manual:** Los archivos generados fueron revisados y ajustados
3. **Decisiones técnicas:** Las decisiones sobre tecnología se basaron en requisitos académicos y buenas prácticas
4. **Documentación:** Se prioriza la claridad y la completitud para facilitar la evaluación

---

## Referencias de Prompts Técnicos

**Patrones de prompt efectivos utilizados:**

- ✅ Especificación clara de requisitos
- ✅ Ejemplos de estructura esperada
- ✅ Referencia a estándares (Docker, pytest, markdown)
- ✅ Contexto académico del proyecto
- ✅ Criterios de aceptación explícitos

---

**Fin del registro de prompts - Sprint 1**

*Este documento será actualizado con nuevos prompts en próximos sprints.*
