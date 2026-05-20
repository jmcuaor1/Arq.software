# Guía de Sustentación — VecinoMarket Entregable 2

## URL de la App
**http://44.207.202.98:8080**

---

## 1. Arquitectura General

El sistema tiene 6 servicios orquestados con Docker Compose:

| Servicio | Tecnología | Puerto interno |
|----------|-----------|---------------|
| `nginx` | Nginx (API Gateway) | 8080 → 80 |
| `api` | Django REST Framework | 8000 |
| `flask_service` | Flask (microservicio) | 5000 |
| `frontend` | React + Vite (build estático en nginx) | 80 |
| `redis` | Redis (message broker) | 6379 |
| `celery_worker` | Celery (tareas asíncronas) | — |

**Flujo de tráfico:**
```
Usuario → Nginx :8080 → /api/* → Django :8000
                       → /flask/* → Flask :5000
                       → /* → React (estático)
```

---

## 2. Patrón Estrangulador (Strangler Pattern)

**Archivo:** `flask_service/app.py`

Las notificaciones fueron **extraídas del monolito Django** y migradas al microservicio Flask independiente.

- **Antes:** Django manejaba notificaciones internamente
- **Ahora:** Flask tiene su propio proceso, puerto y Dockerfile independiente

**Rutas en Nginx** (`nginx/nginx.conf`):
```nginx
location /flask/ {
    proxy_pass http://flask_service:5000/;
}
location /api/v2/notificaciones/ {
    proxy_pass http://flask_service:5000/notificaciones/;
}
```

**Django llama al Flask** vía `FlaskNotifier` en `marketplace/infrastructure/notifiers.py` — no lo hace directamente, lo hace a través de un puerto abstracto (Dependency Inversion).

---

## 3. Nginx como API Gateway

**Archivo:** `nginx/nginx.conf`

Nginx actúa como punto de entrada único que enruta el tráfico:
- `/api/v1/*` → Django (versión explícita)
- `/api/*` → Django (compatibilidad)
- `/flask/*` → Flask microservicio
- `/api/v2/notificaciones/` → Flask (ruta legacy)
- `/*` → React frontend (archivos estáticos)

---

## 4. Patrón Adapter — API de Terceros

**Archivo:** `marketplace/infrastructure/adapters/gemini_adapter.py`

Se implementa el **Patrón Adapter** con **Inversión de Dependencias**:

```
domain/ports.py → DescriptionGeneratorPort (puerto abstracto)
        ↑
GeminiAdapter (implementación concreta en infrastructure/)
```

- El dominio **nunca importa** `google.genai` directamente
- Si se cambia de Gemini a otra IA, solo se cambia el Adapter
- El endpoint es `/api/ai/generar-descripcion/`

**Sustentación del patrón:** Aunque la cuota de la API key esté agotada, el **patrón está implementado correctamente** — el `GeminiAdapter` implementa `DescriptionGeneratorPort`, y retorna `""` con fallback graceful cuando falla.

---

## 5. Servicio Aliado

**Archivos:**
- `marketplace/infrastructure/adapters/allied_service_adapter.py` — **consume** el servicio del equipo aliado
- `marketplace/interface/views.py` → `CatalogoPublicoView` — **expone** nuestro catálogo

**Servicio que exponemos:** `GET /api/aliado/catalogo/`
Retorna todos los productos y servicios en formato JSON estándar para que otros equipos nos consuman.

**Servicio que consumimos:** `GET /api/aliado/datos-externos/`
Llama al endpoint del equipo aliado (`http://54.198.10.181/api/`). Si está caído, retorna `{ disponible: false }` — **fallback graceful** sin romper la app.

---

## 6. Comunicación Asíncrona — Redis + Celery

**Archivo:** `marketplace/application/tasks.py`

Cuando se publica un producto, Django **no espera** a que se envíe la notificación:

```python
# En views.py — dispara la tarea y sigue
enviar_notificacion_async.delay(vendedor.telefono, producto.nombre)
```

La tarea `enviar_notificacion_async` corre en el `celery_worker` en background:
- Llama al `NotifierFactory` que según `NOTIFIER_BACKEND=flask` usa el `FlaskNotifier`
- Reintenta hasta 3 veces si falla
- Si Redis no está disponible, falla silenciosamente (no rompe el POST)

---

## 7. Factory Pattern — Notificador

**Archivo:** `marketplace/infrastructure/factories.py`

```python
NOTIFIER_BACKEND=flask  → FlaskNotifier (llama al microservicio)
NOTIFIER_BACKEND=console → ConsoleNotifier (imprime en logs)
```

Permite cambiar el backend de notificaciones sin tocar código — solo la variable de entorno.

---

## 8. Arquitectura Hexagonal del Backend

```
marketplace/
├── domain/          # Python puro — CERO imports de Django
│   ├── producto.py, servicio.py, usuario.py...
│   ├── builders.py  # Builder Pattern para Producto
│   └── ports.py     # Puertos abstractos (interfaces)
├── application/     # Casos de uso — Services + Commands (DTOs)
│   ├── services.py  # PublicacionService, ServicioService...
│   └── tasks.py     # Celery tasks
├── infrastructure/  # Adaptadores concretos
│   ├── repositories.py    # InMemory repos
│   ├── factories.py       # NotifierFactory
│   └── adapters/          # Gemini, Allied service
└── interface/       # HTTP — DRF Views + Serializers
    ├── views.py
    ├── serializers.py
    └── urls.py
```

**Regla de oro:** Django nunca aparece en `domain/` ni `application/`. Se puede demostrar con `grep -r "from django" marketplace/domain/`.

---

## 9. i18n Bilingüe

**Archivo:** `frontend_react/src/App.jsx`

El frontend tiene un sistema de traducciones propio con el objeto `TRANSLATIONS`:
- Todos los textos de la UI pasan por la función `t('clave')`
- Botón EN/ES en el navbar cambia el idioma en tiempo real
- **Sin textos quemados** en los componentes — todos usan `t()`

El backend usa `gettext` de Django — el `Dockerfile` ejecuta `compilemessages` al construir.

---

## 10. Infraestructura AWS

- **Instancia:** EC2 t3.micro, Amazon Linux 2023
- **IP Elástica:** `44.207.202.98` (fija, no cambia al reiniciar)
- **Puerto público:** 8080 (Security Group abierto)
- **Docker Compose:** 6 servicios levantados con un solo comando

---

## Preguntas frecuentes del profesor

**¿Por qué Flask y no Django para las notificaciones?**
El Strangler Pattern extrae funcionalidades del monolito gradualmente. Flask es más liviano para un microservicio de notificaciones que no necesita ORM ni admin.

**¿Cómo se garantiza que el dominio no depende de Django?**
Las capas `domain/` y `application/` solo usan Python puro y dataclasses. Los repositorios son interfaces abstractas — la implementación en memoria está en `infrastructure/`.

**¿Qué pasa si el equipo aliado está caído?**
`AlliedServiceAdapter` tiene try/except con timeout de 8 segundos — retorna `{ disponible: false }` y el frontend muestra el mensaje de no disponible sin romper la experiencia.

**¿Qué pasa si Redis está caído?**
El `try/except` en `ProductoListView.post` captura cualquier excepción de Celery y la ignora — el producto se publica igual, solo que sin notificación asíncrona.

**¿Cómo funciona el Builder Pattern?**
`ProductoBuilder` en `domain/builders.py` valida cada campo antes de construir el `Producto`. Si algún campo es inválido lanza `ValidationError` antes de que el objeto exista.
