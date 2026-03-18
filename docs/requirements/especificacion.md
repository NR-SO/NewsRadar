# Especificación Técnica - NEWSRADAR

**Versión:** 1.0  
**Fecha:** Marzo 2026  
**Estado:** Draft - Sprint 1

---

## 1. Visión General

NEWSRADAR es un sistema de procesamiento y análisis de canales RSS que:

- Agrega múltiples fuentes RSS en tiempo real
- Clasifica automáticamente noticias según IPTC Media Topics
- Proporciona visualizaciones interactivas del flujo informativo
- Permite gestionar alertas y suscripciones por categoría

---

## 2. Requisitos Funcionales

### RF-001: Agregar fuentes RSS

**Descripción:** El sistema debe permitir agregar, editar y eliminar canales RSS.

**Criterios de aceptación:**
- ✅ Usuario puede agregar URL de feed RSS
- ✅ Sistema valida la URL y conecta con la fuente
- ✅ Se almacenan metadatos del canal
- ✅ El sistema notifica si la fuente es inaccesible

**Endpoint API:** `POST /api/v1/sources`

---

### RF-002: Procesar feeds RSS

**Descripción:** El sistema procesa periódicamente cada feed para obtener nuevos artículos.

**Criterios de aceptación:**
- ✅ Polling automático cada N horas
- ✅ Extrae: título, descripción, link, fecha, autor
- ✅ Evita duplicados mediante hash de contenido
- ✅ Almacena artículos en BD

**Proceso:**
1. Consultar MongoDB scheduleador
2. Descargar feed XML/RSS
3. Parsear con feedparser
4. Validar artículos
5. Persistir en BD

---

### RF-003: Clasificar con IPTC Media Topics

**Descripción:** Cada artículo es clasificado automáticamente en categorías IPTC.

**Criterios de aceptación:**
- ✅ Clasificación basada en título + descripción
- ✅ Soporte para múltiples categorías por artículo
- ✅ Confidence score (0-1)
- ✅ Permite override manual

**Categorías IPTC:**
- 01000000: Arts, Culture, Entertainment, Sports
- 02000000: Business, Economics, Finance
- 03000000: Disasters, Accidents
- 04000000: Environment, Nature
- 05000000: Health
- 06000000: Politics
- 07000000: Science, Education, Technology
- 08000000: Social Issues
- 09000000: Conflict, War, Peace
- 10000000: Religion

---

### RF-004: Visualización interactiva

**Descripción:** Dashboard con visualizaciones D3.js de flujos de noticias.

**Criterios de aceptación:**
- ✅ Timeline interactivo de artículos
- ✅ Nube de categorías IPTC
- ✅ Gráficos de tendencias por tema
- ✅ Filtrado por fecha, categoría, fuente

---

### RF-005: Alertas y notificaciones

**Descripción:** Los usuarios pueden recibir alertas cuando aparecen noticias de categorías seleccionadas.

**Criterios de aceptación:**
- ✅ Crear suscripción por categoría IPTC
- ✅ Notificaciones en tiempo real (WebSocket)
- ✅ Email opcional
- ✅ Gestionar preferencias de alertas

---

## 3. Requisitos No Funcionales

### RNF-001: Rendimiento
- **Objetivo:** La página de inicio debe cargar en < 2 segundos
- **Métrica:** Lighthouse score > 80

### RNF-002: Escalabilidad
- **Objetivo:** Soportar 1M+ artículos en BD
- **Métrica:** Query de último artículo < 100ms

### RNF-003: Disponibilidad
- **Objetivo:** 99.5% uptime en producción
- **Métrica:** Monitoreado con health checks

### RNF-004: Seguridad
- **Objetivo:** Proteger datos sensibles de usuarios
- **Métrica:** 
  - Autenticación JWT
  - HTTPS en producción
  - Validación de input

### RNF-005: Mantenibilidad
- **Objetivo:** Tests > 70% de cobertura
- **Métrica:** Reporte de cobertura de pytest

---

## 4. Arquitectura del Sistema

```
┌─────────────┐
│   Frontend  │
│  (React)    │
└──────┬──────┘
       │ HTTP/WebSocket
┌──────▼──────────────┐
│  API Gateway        │  (Nginx - tiempo real)
│  (FastAPI)          │
└──────┬──────────────┘
       │
   ┌───┴───┐
   │       │
┌──▼─┐  ┌──▼─┐
│RSS │  │IPTC│
│Feed│  │Cla-│
│ Proc.  │sif.│
└──┬─┘  └──┬─┘
   │       │
   └───┬───┘
       │
   ┌───▼──────┐
   │ MongoDB  │
   │    DB    │
   └──────────┘
```

---

## 5. Modelos de Datos

### Colección: `sources`

```json
{
  "_id": ObjectId,
  "name": "BBC News",
  "url": "http://feeds.bbc.co.uk/news/rss.xml",
  "category": "General News",
  "active": true,
  "lastUpdated": ISODate,
  "nextUpdate": ISODate,
  "updateFrequency": "hourly"
}
```

### Colección: `articles`

```json
{
  "_id": ObjectId,
  "title": "Article Title",
  "description": "Short description",
  "link": "https://...",
  "author": "Author Name",
  "pubDate": ISODate,
  "sourceId": ObjectId,
  "content": "Full content",
  "image": "https://...",
  "iptcTopics": [
    {
      "code": "02001000",
      "name": "Business",
      "confidence": 0.95,
      "manual": false
    }
  ],
  "hash": "sha256hash",
  "createdAt": ISODate,
  "updatedAt": ISODate
}
```

### Colección: `users`

```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password": "bcrypt_hash",
  "preferences": {
    "iptcSubscriptions": ["02001000", "07003000"],
    "sourceSubscriptions": [ObjectId, ...],
    "alertsEnabled": true,
    "emailNotifications": false
  },
  "createdAt": ISODate,
  "lastLogin": ISODate
}
```

---

## 6. Endpoints API (Sprint 1)

### Health Check
- `GET /health` → Status 200

### Root
- `GET /` → Welcome message

### Sources (Future)
- `GET /api/v1/sources` → List sources
- `POST /api/v1/sources` → Create source
- `PUT /api/v1/sources/{id}` → Update source
- `DELETE /api/v1/sources/{id}` → Delete source

### Articles (Future)
- `GET /api/v1/articles` → List articles (paginated)
- `GET /api/v1/articles/{id}` → Get article detail
- `GET /api/v1/articles/search` → Search articles

### Topics (Future)
- `GET /api/v1/topics` → List IPTC topics

---

## 7. Dependencias Clave

### Backend
```
fastapi==0.104.1
uvicorn==0.24.0
pymongo==4.6.0
feedparser==6.0.10
pydantic==2.5.0
python-jose==3.3.0
passlib==1.7.4
```

### Frontend
```
react@18.2.0
react-dom@18.2.0
d3@7.8.5
axios@1.6.2
react-router-dom@6.20.0
```

---

## 8. Cronograma de Implementación

| Sprint | Objetivo | Duración |
|--------|----------|----------|
| 1 | Base técnica + setup | 2 semanas |
| 2 | Backend + RSS processing | 2 semanas |
| 3 | IPTC classification | 2 semanas |
| 4 | Frontend + visualizaciones | 2 semanas |
| 5 | Refinamiento + deploy | 1 semana |

---

## 9. Estrategia de Testing

### Unit Tests (pytest)
- Tests de endpoints FastAPI
- Tests de utilidades
- Cobertura objetivo: 70%

### Integration Tests
- Tests de conexión MongoDB
- Tests de feed processing
- Tests de clasificación IPTC

### E2E Tests
- Tests de flujo completo mediante Selenium

---

## 10. Seguridad

- [ ] Input validation en todos los endpoints
- [ ] CORS configurado correctamente
- [ ] JWT tokens con expiración
- [ ] Contraseñas hasheadas con bcrypt
- [ ] HTTPS en producción
- [ ] Rate limiting en endpoints públicos
- [ ] Validación de URLs de RSS

---

## 11. Deployment

### Desarrollo
```bash
docker-compose up -d
```

### Producción
- [ ] Configurar variables de entorno seguras
- [ ] Habilitar HTTPS
- [ ] Configurar backups automáticos MongoDB
- [ ] Monitoreo con Prometheus/Grafana
- [ ] Logs centralizados con ELK

---

## 12. Métricas y KPIs

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| Uptime | 99.5% | TBD |
| Response time (p95) | < 500ms | TBD |
| Articles processed/hora | 1000+ | TBD |
| Test coverage | > 70% | TBD |
| Build time | < 5 min | TBD |

---

## Próximas fases

- Sprint 2 onwards: Implementación según especificación
- Feedback iterativo del equipo docente
- Ajustes según resultados de testing
