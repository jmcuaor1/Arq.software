# Guía de Inicio

## Opción A — Docker (Recomendado)

Levanta todos los servicios con un solo comando desde la raíz del proyecto:

```bash
docker-compose up
```

Esto inicia Django (:8000), React (:5173), Flask (:5000) y Nginx (:8080) en la misma red.
La aplicación completa queda disponible en `http://localhost:8080`.

Para reconstruir imágenes después de cambiar dependencias:

```bash
docker-compose up --build
```

---

## Opción B — Local (Desarrollo)

Requiere tres terminales simultáneas.

### Terminal 1 — Backend Django

```bash
# Activar entorno virtual
.\.venv\Scripts\activate          # Windows
source .venv/bin/activate         # macOS/Linux

pip install -r requirements.txt
python manage.py runserver        # http://localhost:8000
```

### Terminal 2 — Frontend React

```bash
cd frontend_react
npm install
npm run dev                       # http://localhost:5173
```

### Terminal 3 — Microservicio Flask

```bash
cd flask_service
pip install -r requirements.txt
python app.py                     # http://localhost:5000
```

---

## Requisitos Previos

- Python 3.10+
- Node.js 18+ (incluye npm)
- Docker + Docker Compose (para Opción A)

---

## Notas

- **Persistencia**: Los repositorios son in-memory. Reiniciar Django borra los datos, excepto los datos de prueba que se cargan automáticamente al arrancar.
- **CORS**: `CORS_ALLOW_ALL_ORIGINS = True` en `core/settings.py`. No usar en producción.
- **Pruebas de lógica**: `python tests_backend/test_logic.py` ejecuta el flujo completo sin Django ni HTTP.
