# Pipeline CI/CD para NEWSRADAR

Este directorio contiene las definiciones de flujos de trabajo automatizados de GitHub Actions.

## Archivos

- `ci-cd.yml`: Pipeline principal de integración continua y despliegue continuo.

## Descripción del Pipeline CI/CD

El pipeline ejecuta:

1. Tests unitarios
2. Tests funcionales
3. Generación de reporte de cobertura
4. Build de contenedores Docker

## Ejecución

Los flujos se ejecutan automáticamente cuando se hace:
- Push a la rama main
- Push a la rama develop
- Pull request a main o develop

## Estados

- Test: Ejecución de pruebas unitarias y funcionales
- Build: Construcción de contenedores Docker
