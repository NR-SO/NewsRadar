# 0001 - Decisión Arquitectónica: Selección de Tecnologías Base

**Status:** Aceptada  
**Date:** Marzo 2026  
**Authors:** NEWSRADAR Team  
**Context:** Decisión sobre el stack tecnológico para el proyecto académico NEWSRADAR.

---

## Problema

Necesitamos seleccionar un stack tecnológico que cumpla con los siguientes requisitos:

1. **Requisitos técnicos:**
   - Procesamiento de múltiples fuentes RSS
   - Clasificación automática con IPTC Media Topics
   - Visualización interactiva en tiempo real
   - Arquitectura escalable y mantenible
   - Facilidad para la integración CI/CD

2. **Requisitos académicos:**
   - Tecnologías populares en la industria
   - Buena documentación disponible
   - Comunidad activa
   - Relevancia para la asignatura

---

## Decisión

Se ha seleccionado el siguiente stack:

### Backend: **FastAPI + Python**

**Rationale:**
- Framework asincrónico moderno con excelente rendimiento
- Integración nativa con OpenAPI/Swagger para documentación automática
- Ideal para procesamiento de datos RSS en tiempo real
- Excelente soporte para dependencias inyectables y testing
- Comunidad activa y documentación completa

**Versión:** Python 3.11+, FastAPI 0.104+

---

### Base de Datos: **MongoDB**

**Rationale:**
- Estructura flexible para documentos RSS de diversas fuentes
- Excelente para almacenar clasificaciones IPTC
- Escalabilidad horizontal simple
- Menos rigidez que SQL para datos semiestructurados
- Facilita iteración rápida en desarrollo académico

**Alternativas consideradas:**
- PostgreSQL: Más rígido, menos flexible para esquemas variados
- Cassandra: Demasiado complejo para un proyecto académico

**Versión:** MongoDB 7.0+

---

### Frontend: **React + D3.js**

**Rationale:**
- React: Biblioteca moderna y popular para UIs interactivas
- Componentes reutilizables y gestión de estado (Zustand)
- D3.js: Librería estándar para visualizaciones de datos complejas
- Visualización de flujos de noticias y clasificaciones IPTC
- Compatible con herramientas de desarrollo modernas (Vite)

**Alternativas consideradas:**
- Angular: Mayor curva de aprendizaje, overhead innecesario
- Vue.js: Menos popular en la industria
- Svelte: Comunidad más pequeña

**Versión:** React 18+, D3.js 7+

---

### Contenedorización: **Docker + Docker Compose**

**Rationale:**
- Garantiza compatibilidad entre entornos (desarrollo, testing, producción)
- Facilita la evaluación del proyecto (reproduciblidad)
- Estándar de la industria para microservicios
- Integración simple con CI/CD

**Versión:** Docker 20+, Docker Compose 1.29+

---

### Testing: **pytest + Jest**

**Rationale:**
- pytest: Framework estándar en Python, fácil de usar
- Jest: Popular para testing en React
- Ambos con excelente integración con CI/CD

---

### CI/CD: **GitHub Actions**

**Rationale:**
- Integrado con el repositorio GitHub del proyecto
- Gratuito para repositorios públicos
- Suficiente para un proyecto académico

---

## Consecuencias

### Positivas

✅ Stack moderno y relevante industrialmente  
✅ Excelente rendimiento para aplicaciones IoT/tiempo real  
✅ Comunidades activas y amplia documentación  
✅ Herramientas modernas para desarrollo y testing  
✅ Facilita scalabilidad futura  
✅ Buena integración con herramientas de IA (GPT assistants)

### Negativas/Riesgos

⚠️ Mayor overhead inicial de configuración Docker  
⚠️ Menos control fino que alternativas como Angular/ASP.NET  
⚠️ MongoDB requiere cuidado con indexes en grandes volúmenes  
⚠️ Curva de aprendizaje para D3.js  

---

## Alternativas Rechazadas

| Opción | Razón del rechazo |
|--------|-------------------|
| Node.js + Express | Menos control de tipos, menos estructurado que FastAPI |
| Spring Boot + Java | Demasiado pesado para proyecto académico |
| ASP.NET Core | No es el estándar en contexto académico universitario |
| Redis como BD | Insuficiente para persistencia de datos complejos |

---

## Validación

Esta decisión será validada por:
1. Éxito en Sprint 1 (setup básico)
2. Capacidad de implementar requisitos en Sprint 2-4
3. Feedback del equipo docente
4. Performance en tests unitarios y funcionales

---

## Referencias

- FastAPI: https://fastapi.tiangolo.com/
- MongoDB: https://www.mongodb.com/
- React: https://react.dev/
- D3.js: https://d3js.org/
- Docker: https://www.docker.com/
- GitHub Actions: https://github.com/features/actions
