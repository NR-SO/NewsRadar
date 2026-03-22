// Script de inicialización para MongoDB - NEWSRADAR
// Ejecutado automáticamente al crear el contenedor por primera vez
// Crea colecciones con validación de esquema, índices y datos semilla

db = db.getSiblingDB('newsradar_db');

// ============================================================
// COLECCIÓN: users
// Roles: "manager" (gestiona alertas y fuentes) | "reader" (solo lectura)
// ============================================================
try {
  db.createCollection("users", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["email", "password", "name", "role"],
        properties: {
          email:    { bsonType: "string", description: "Email único del usuario" },
          password: { bsonType: "string", description: "Hash bcrypt de la contraseña" },
          name:     { bsonType: "string", description: "Nombre completo" },
          role:     { enum: ["gestor_newsradar", "lector"], description: "Rol del usuario" },
          active:   { bsonType: "bool" },
          preferences: {
            bsonType: "object",
            properties: {
              iptcSubscriptions:  { bsonType: "array" },
              sourceSubscriptions:{ bsonType: "array" },
              alertsEnabled:      { bsonType: "bool" },
              emailNotifications: { bsonType: "bool" },
              language:           { enum: ["es", "en"] }
            }
          },
          createdAt: { bsonType: "date" },
          lastLogin: { bsonType: "date" }
        }
      }
    }
  });
  print("✓ Colección 'users' creada");
} catch (e) {
  print("  Colección 'users' ya existe, aplicando validador...");
  db.runCommand({
    collMod: "users",
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["email", "password", "name", "role"]
      }
    }
  });
}

// ============================================================
// COLECCIÓN: alerts
// Máx. 20 alertas por manager. Keywords con sinónimos (3-10).
// ============================================================
try {
  db.createCollection("alerts", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["name", "ownerId", "keywords"],
        properties: {
          name:    { bsonType: "string", description: "Nombre descriptivo de la alerta" },
          ownerId: { bsonType: "string", description: "ID del manager propietario" },
          keywords: {
            bsonType: "array",
            description: "Términos de búsqueda con sinónimos",
            items: {
              bsonType: "object",
              required: ["term"],
              properties: {
                term:     { bsonType: "string" },
                synonyms: { bsonType: "array", items: { bsonType: "string" } }
              }
            }
          },
          iptcTopics: { bsonType: "array", items: { bsonType: "string" }, description: "Códigos IPTC" },
          active:     { bsonType: "bool" },
          matchCount: { bsonType: "int", description: "Número de coincidencias acumuladas" },
          createdAt:  { bsonType: "date" },
          updatedAt:  { bsonType: "date" }
        }
      }
    }
  });
  print("✓ Colección 'alerts' creada");
} catch (e) {
  print("  Colección 'alerts' ya existe");
}

// ============================================================
// COLECCIÓN: sources (fuentes RSS)
// ============================================================
try {
  db.createCollection("sources", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["name", "url", "category", "active"],
        properties: {
          name:        { bsonType: "string" },
          url:         { bsonType: "string", description: "URL del feed RSS" },
          mediaOutlet: { bsonType: "string", description: "Medio de comunicación" },
          category:    { bsonType: "string" },
          iptcCode:    { bsonType: "string", description: "Código IPTC de primer nivel" },
          language:    { enum: ["es", "en", "fr", "de", "it", "pt"] },
          active:      { bsonType: "bool" },
          updateFrequency: { enum: ["hourly", "daily", "weekly"] },
          lastUpdated: { bsonType: "date" },
          nextUpdate:  { bsonType: "date" },
          createdAt:   { bsonType: "date" },
          updatedAt:   { bsonType: "date" }
        }
      }
    }
  });
  print("✓ Colección 'sources' creada");
} catch (e) {
  print("  Colección 'sources' ya existe");
}

// ============================================================
// COLECCIÓN: articles (noticias indexadas)
// ============================================================
try {
  db.createCollection("articles", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["title", "sourceId", "pubDate"],
        properties: {
          title:       { bsonType: "string" },
          description: { bsonType: "string" },
          content:     { bsonType: "string" },
          link:        { bsonType: "string" },
          author:      { bsonType: "string" },
          pubDate:     { bsonType: "date" },
          sourceId:    { bsonType: "objectId" },
          image:       { bsonType: "string" },
          hash:        { bsonType: "string", description: "SHA256 para deduplicación" },
          language:    { bsonType: "string" },
          iptcTopics: {
            bsonType: "array",
            items: {
              bsonType: "object",
              properties: {
                code:       { bsonType: "string" },
                name:       { bsonType: "string" },
                confidence: { bsonType: "double" },
                manual:     { bsonType: "bool" }
              }
            }
          },
          alertMatches: { bsonType: "array", items: { bsonType: "string" }, description: "IDs de alertas que coinciden" },
          createdAt:   { bsonType: "date" },
          updatedAt:   { bsonType: "date" }
        }
      }
    }
  });
  print("✓ Colección 'articles' creada");
} catch (e) {
  print("  Colección 'articles' ya existe");
}

// ============================================================
// ÍNDICES - Optimización de consultas
// ============================================================

// users
db.users.createIndex({ "email": 1 }, { unique: true, name: "idx_users_email" });
db.users.createIndex({ "role": 1 }, { name: "idx_users_role" });
print("✓ Índices 'users' creados");

// alerts
db.alerts.createIndex({ "ownerId": 1 }, { name: "idx_alerts_owner" });
db.alerts.createIndex({ "active": 1 }, { name: "idx_alerts_active" });
db.alerts.createIndex({ "iptcTopics": 1 }, { name: "idx_alerts_iptc" });
print("✓ Índices 'alerts' creados");

// sources
db.sources.createIndex({ "url": 1 }, { unique: true, name: "idx_sources_url" });
db.sources.createIndex({ "active": 1, "nextUpdate": 1 }, { name: "idx_sources_active_next" });
db.sources.createIndex({ "iptcCode": 1 }, { name: "idx_sources_iptc" });
db.sources.createIndex({ "language": 1 }, { name: "idx_sources_lang" });
print("✓ Índices 'sources' creados");

// articles - índices de búsqueda e indexación
db.articles.createIndex({ "hash": 1 }, { unique: true, name: "idx_articles_hash" });
db.articles.createIndex({ "sourceId": 1, "pubDate": -1 }, { name: "idx_articles_source_date" });
db.articles.createIndex({ "pubDate": -1 }, { name: "idx_articles_date" });
db.articles.createIndex({ "iptcTopics.code": 1 }, { name: "idx_articles_iptc" });
db.articles.createIndex({ "alertMatches": 1 }, { name: "idx_articles_alerts" });
// Índice de texto completo para búsqueda semántica (equivalente a Elasticsearch básico)
db.articles.createIndex(
  { "title": "text", "description": "text", "content": "text" },
  { name: "idx_articles_fulltext", weights: { title: 10, description: 5, content: 1 }, default_language: "english" }
);
print("✓ Índices 'articles' creados (incluye búsqueda de texto completo)");

// ============================================================
// DATOS SEMILLA - Fuentes RSS (se insertan si la colección está vacía)
// 10+ medios de comunicación, cobertura de categorías IPTC principales
// ============================================================
if (db.sources.countDocuments() === 0) {
  var now = new Date();
  db.sources.insertMany([
    // --- BBC News (Reino Unido) ---
    { name: "BBC News - Top Stories", url: "http://feeds.bbc.co.uk/news/rss.xml", mediaOutlet: "BBC News", category: "General News", iptcCode: "11000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "BBC News - Technology", url: "http://feeds.bbc.co.uk/news/technology/rss.xml", mediaOutlet: "BBC News", category: "Technology", iptcCode: "13000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "BBC News - Science & Environment", url: "http://feeds.bbc.co.uk/news/science_and_environment/rss.xml", mediaOutlet: "BBC News", category: "Science", iptcCode: "15000000", language: "en", active: true, updateFrequency: "daily", createdAt: now, updatedAt: now },
    { name: "BBC News - Business", url: "http://feeds.bbc.co.uk/news/business/rss.xml", mediaOutlet: "BBC News", category: "Business", iptcCode: "04000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "BBC News - Sport", url: "http://feeds.bbc.co.uk/sport0/rss/1.0/sportonline_uk_all.xml", mediaOutlet: "BBC News", category: "Sports", iptcCode: "15000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },

    // --- Reuters (Internacional) ---
    { name: "Reuters - World News", url: "https://feeds.reuters.com/reuters/worldNews", mediaOutlet: "Reuters", category: "World", iptcCode: "11000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "Reuters - Business", url: "https://feeds.reuters.com/reuters/businessNews", mediaOutlet: "Reuters", category: "Business", iptcCode: "04000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "Reuters - Technology", url: "https://feeds.reuters.com/reuters/technologyNews", mediaOutlet: "Reuters", category: "Technology", iptcCode: "13000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },

    // --- The Guardian (Reino Unido) ---
    { name: "The Guardian - World", url: "https://www.theguardian.com/world/rss", mediaOutlet: "The Guardian", category: "World", iptcCode: "11000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "The Guardian - Business", url: "https://www.theguardian.com/business/rss", mediaOutlet: "The Guardian", category: "Business", iptcCode: "04000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "The Guardian - Science", url: "https://www.theguardian.com/science/rss", mediaOutlet: "The Guardian", category: "Science", iptcCode: "15000000", language: "en", active: true, updateFrequency: "daily", createdAt: now, updatedAt: now },
    { name: "The Guardian - Environment", url: "https://www.theguardian.com/environment/rss", mediaOutlet: "The Guardian", category: "Environment", iptcCode: "06000000", language: "en", active: true, updateFrequency: "daily", createdAt: now, updatedAt: now },

    // --- Al Jazeera (Internacional) ---
    { name: "Al Jazeera - All News", url: "https://www.aljazeera.com/xml/rss/all.xml", mediaOutlet: "Al Jazeera", category: "World", iptcCode: "11000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },

    // --- NPR (Estados Unidos) ---
    { name: "NPR - Top Stories", url: "https://feeds.npr.org/1001/rss.xml", mediaOutlet: "NPR", category: "General News", iptcCode: "11000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "NPR - Health", url: "https://feeds.npr.org/1128/rss.xml", mediaOutlet: "NPR", category: "Health", iptcCode: "07000000", language: "en", active: true, updateFrequency: "daily", createdAt: now, updatedAt: now },
    { name: "NPR - Science", url: "https://feeds.npr.org/1007/rss.xml", mediaOutlet: "NPR", category: "Science", iptcCode: "15000000", language: "en", active: true, updateFrequency: "daily", createdAt: now, updatedAt: now },

    // --- TechCrunch (Tecnología) ---
    { name: "TechCrunch - Latest", url: "http://feeds.feedburner.com/TechCrunch/", mediaOutlet: "TechCrunch", category: "Technology", iptcCode: "13000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "TechCrunch - Startups", url: "http://feeds.feedburner.com/TechCrunch/startups", mediaOutlet: "TechCrunch", category: "Business", iptcCode: "04000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },

    // --- Wired (Tecnología) ---
    { name: "Wired - Latest", url: "https://www.wired.com/feed/rss", mediaOutlet: "Wired", category: "Technology", iptcCode: "13000000", language: "en", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },

    // --- NASA (Ciencia) ---
    { name: "NASA - Breaking News", url: "https://www.nasa.gov/rss/dyn/breaking_news.rss", mediaOutlet: "NASA", category: "Science", iptcCode: "15000000", language: "en", active: true, updateFrequency: "daily", createdAt: now, updatedAt: now },

    // --- El País (España) ---
    { name: "El País - Portada", url: "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada", mediaOutlet: "El País", category: "General News", iptcCode: "11000000", language: "es", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "El País - Tecnología", url: "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/tecnologia/portada", mediaOutlet: "El País", category: "Technology", iptcCode: "13000000", language: "es", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },
    { name: "El País - Economía", url: "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/economia/portada", mediaOutlet: "El País", category: "Business", iptcCode: "04000000", language: "es", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },

    // --- Le Monde (Francia) ---
    { name: "Le Monde - À la une", url: "https://www.lemonde.fr/rss/une.xml", mediaOutlet: "Le Monde", category: "General News", iptcCode: "11000000", language: "fr", active: true, updateFrequency: "hourly", createdAt: now, updatedAt: now },

    // --- The Economist (Internacional) ---
    { name: "The Economist - World this Week", url: "https://www.economist.com/the-world-this-week/rss.xml", mediaOutlet: "The Economist", category: "Politics/Economics", iptcCode: "11000000", language: "en", active: true, updateFrequency: "weekly", createdAt: now, updatedAt: now }
  ]);
  print("✓ " + db.sources.countDocuments() + " fuentes RSS insertadas (seed)");
} else {
  print("  Fuentes RSS ya existen (" + db.sources.countDocuments() + " registros), omitiendo seed");
}

// ============================================================
// NOTA SOBRE USUARIOS SEMILLA
// Los usuarios se crean mediante el script Python scripts/seed_db.py
// para garantizar el hash correcto de contraseñas con bcrypt.
// Credenciales por defecto:
//   Admin Manager: admin@newsradar.com / admin123
//   Reader:        reader@newsradar.com / reader123
// ============================================================
print("⚠  Usuarios semilla: ejecutar 'docker exec newsradar-backend python /app/scripts/seed_db.py'");
print("✓ Inicialización de base de datos completada");
