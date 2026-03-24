from app.main import app
import json
import os

os.makedirs("docs/openapi", exist_ok=True)

with open("docs/openapi/openapi.json", "w") as f:
    json.dump(app.openapi(), f, indent=4)

print("✔ OpenAPI generado desde FastAPI")