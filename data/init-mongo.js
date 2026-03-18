// Script de inicialización para MongoDB
// Crea colecciones y datos iniciales

db = db.getSiblingDB('newsradar_db');

// Crear colección de fuentes RSS
db.createCollection("sources", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "url", "category", "active"],
      properties: {
        _id: { bsonType: "objectId" },
        name: { bsonType: "string", description: "Nombre de la fuente" },
        url: { bsonType: "string", description: "URL del feed RSS" },
        category: { bsonType: "string", description: "Categoría general" },
        active: { bsonType: "bool", description: "La fuente está activa" },
        lastUpdated: { bsonType: "date", description: "Última actualización" },
        nextUpdate: { bsonType: "date", description: "Próxima actualización" },
        updateFrequency: { 
          enum: ["hourly", "daily", "weekly"],
          description: "Frecuencia de actualización"
        },
        createdAt: { bsonType: "date" },
        updatedAt: { bsonType: "date" }
      }
    }
  }
});

// Crear colección de artículos
db.createCollection("articles", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["title", "sourceId", "pubDate"],
      properties: {
        _id: { bsonType: "objectId" },
        title: { bsonType: "string" },
        description: { bsonType: "string" },
        content: { bsonType: "string" },
        link: { bsonType: "string" },
        author: { bsonType: "string" },
        pubDate: { bsonType: "date" },
        sourceId: { bsonType: "objectId" },
        image: { bsonType: "string" },
        hash: { bsonType: "string", description: "SHA256 del contenido" },
        iptcTopics: {
          bsonType: "array",
          items: {
            bsonType: "object",
            properties: {
              code: { bsonType: "string" },
              name: { bsonType: "string" },
              confidence: { bsonType: "double" },
              manual: { bsonType: "bool" }
            }
          }
        },
        createdAt: { bsonType: "date" },
        updatedAt: { bsonType: "date" }
      }
    }
  }
});

// Crear colección de usuarios
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "password"],
      properties: {
        _id: { bsonType: "objectId" },
        email: { bsonType: "string" },
        password: { bsonType: "string" },
        preferences: {
          bsonType: "object",
          properties: {
            iptcSubscriptions: { bsonType: "array" },
            sourceSubscriptions: { bsonType: "array" },
            alertsEnabled: { bsonType: "bool" },
            emailNotifications: { bsonType: "bool" }
          }
        },
        createdAt: { bsonType: "date" },
        lastLogin: { bsonType: "date" }
      }
    }
  }
});

// Crear índices para optimización
db.articles.createIndex({ "sourceId": 1, "pubDate": -1 });
db.articles.createIndex({ "hash": 1 }, { unique: true });
db.articles.createIndex({ "iptcTopics.code": 1 });
db.articles.createIndex({ "pubDate": -1 });

db.sources.createIndex({ "url": 1 }, { unique: true });
db.sources.createIndex({ "active": 1, "nextUpdate": 1 });

db.users.createIndex({ "email": 1 }, { unique: true });

print("✓ Base de datos inicializada correctamente");
