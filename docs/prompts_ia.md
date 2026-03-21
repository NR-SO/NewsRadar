# Registro de Uso de IA (Prompts) - NEWSRADAR

**Objetivo:** Mantener la trazabilidad del uso de herramientas de Inteligencia Artificial Generativa durante el desarrollo del proyecto académico NEWSRADAR, detallando los prompts clave utilizados para la generación de código, configuración y documentación.

**Versión:** 1.0  
**Última actualización:** 21 de Marzo de 2026

---

## Resumen de Uso por Sprints

### Sprint 1: Base técnica y repositorio

Durante este sprint, la IA se utilizó principalmente para acelerar el proceso de *scaffolding* (creación de estructura), redacción de *boilerplate* (código repetitivo de configuración) y resolución de conflictos de dependencias en Docker y Node.js.

| Fase | Objetivo | Prompt Principal / Contexto proporcionado a la IA | Resultado Obtenido |
| :--- | :--- | :--- | :--- |
| **Estructura** | Generar el árbol de directorios base. | *"Genera un script bash para crear la estructura de carpetas (src, docs, scripts, tests, config, data) para un proyecto FastAPI + React."* | Script `init_structure.sh` ejecutado exitosamente. |
| **Infraestructura** | Crear los Dockerfiles y el orquestador. | *"Crea dos Dockerfiles multi-stage optimizados (Python 3.11 para backend, Node 18 para frontend) y un docker-compose.yml que incluya MongoDB 7.0."* | Archivos de configuración Docker base generados. |
| **Documentación** | Redactar el ADR fundacional. | *"Crea un Architecture Decision Record (ADR-0001) justificando FastAPI, MongoDB y React para un proyecto de procesamiento RSS."* | Archivo `0001-arquitectura-base.md` estructurado. |
| **Documentación** | Especificación técnica inicial. | *"Crea un documento de especificación técnica incluyendo RFs (procesamiento RSS, clasificación IPTC), RNFs y modelos de datos básicos."* | Archivo `especificacion.md` redactado. |
| **Debugging** | Resolver conflicto de dependencias (React). | *"Al hacer build del frontend en Docker, obtengo: 'ERESOLVE could not resolve... Conflicting peer dependency' con ajv y ajv-keywords."* | Diagnóstico del problema de *hoisting* y ajuste de versiones en `package.json`. |
| **Debugging** | Solucionar error de compilación (Webpack). | *"Sigue fallando con: 'Error: Cannot find module ajv/dist/compile/codegen'."* | Corrección final ajustando la versión exacta de TypeScript a `4.9.5` compatible con `react-scripts@5.0.1`. |
| **CI/CD** | Configurar GitHub Actions. | *"Genera un pipeline básico en GitHub Actions (ci.yml) que levante el entorno y corra pytest en el backend."* | Pipeline `.github/workflows/ci.yml` funcional. |
| **Documentación** | Cierre de documentación. | *"Actualiza el README.md para incluir instrucciones exactas de clonación, 1 comando de ejecución (docker-compose up), test y deploy."* | `README.md` final completado y formateado. |

---

## Consideraciones Metodológicas

1. **Iteración:** La IA se utilizó como herramienta de asistencia ("pair programming"), no como reemplazo del criterio técnico. La mayoría de los outputs requirieron entre 1 y 2 iteraciones manuales para ajustarse al contexto estricto de la asignatura.
2. **Validación:** Todo el código generado (especialmente las configuraciones de Docker y los scripts) fue probado localmente antes de ser integrado (mergeado) en la rama principal.
3. **Decisiones Arquitectónicas:** Las decisiones de stack tecnológico fueron tomadas por el equipo; la IA se utilizó únicamente para formatear la justificación de dichas decisiones en formato ADR estándar.

---
*Este documento es vivo y se actualizará al finalizar cada Sprint.*