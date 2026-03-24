# ---------------- CONFIG ----------------

PYTHON=python3

all: build test docs

# ---------------- BUILD ----------------
build:
	@echo "🔧 Instalando dependencias..."
	@if [ -f requirements.txt ]; then pip install -r requirements.txt; else echo "No requirements.txt found"; fi

# ---------------- TEST ----------------
test:
	@echo "🧪 Ejecutando tests..."
	@if [ -f scripts/test.sh ]; then bash scripts/test.sh; \
	elif [ -f scripts/test.bat ]; then scripts/test.bat; \
	else pytest tests/; fi

# ---------------- DOCS ----------------
docs:
	@echo "📄 Generando documentación OpenAPI..."
	@if [ -f scripts/generate_docs.py ]; then python scripts/generate_docs.py; \
	else echo "No docs script yet"; fi

# ---------------- RUN ----------------
run:
	@echo "🚀 Ejecutando aplicación..."
	@if [ -f scripts/run.sh ]; then bash scripts/run.sh; \
	else echo "No run script found"; fi

# ---------------- CLEAN ----------------
clean:
	@echo "🧹 Limpiando archivos temporales..."
	rm -rf __pycache__ .pytest_cache

# ---------------- HELP ----------------
help:
	@echo "Comandos disponibles:"
	@echo "  make        -> build + test + docs"
	@echo "  make build  -> instalar dependencias"
	@echo "  make test   -> ejecutar tests"
	@echo "  make docs   -> generar OpenAPI"
	@echo "  make run    -> ejecutar app"
	@echo "  make clean  -> limpiar temporales"