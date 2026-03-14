# Documentación del Backend (Django APIs)

El backend de VecinoMarket funciona como una **API REST (Headless)** que procesa peticiones JSON del frontend de React.

##  Configuración de Red: CORS
Para permitir que React (puerto 5173) hable con Django (puerto 8000), hemos implementado `django-cors-headers`.
*   **Configuración**: En `settings.py`, se añadió `CorsMiddleware`.
*   **Permisos**: Actualmente está configurado con `CORS_ALLOW_ALL_ORIGINS = True` para facilitar el desarrollo local.

---

##  Endpoints Disponibles
Todos los endpoints están prefijados con `/api/`:

| Método | Endpoint | Descripción | Serializer Usado |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/productos/` | Lista todos los productos disponibles. | `ProductoSerializer` |
| `POST` | `/api/productos/` | Publica un nuevo producto. | `PublicarProductoSerializer` |
| `GET` | `/api/servicios/` | Lista todos los servicios ofrecidos. | `ServicioSerializer` |
| `POST` | `/api/servicios/` | Registra un nuevo servicio. | `PublicarServicioSerializer` |
| `POST` | `/api/consultas/` | Envía un mensaje a un vendedor/proveedor. | `RegistrarConsultaSerializer` |

---

##  Capa de Presentación (Views)
Ubicación: `marketplace/interface/views.py`

Las vistas son **"Thin Controllers"** (controladores delgados). Su única responsabilidad es:
1.  Recibir la petición HTTP.
2.  Validar los datos usando **Serializers**.
3.  Mapear los datos a un **Comando**.
4.  Llamar al **Servicio de Aplicación** correspondiente.
5.  Retornar una respuesta JSON.

---

##  Datos de Prueba (Mocking)
Para facilitar las pruebas sin una base de datos persistente, el sistema inicializa automáticamente datos de prueba en `views.py`:
*   **user-001**: Juan Pérez.
*   **user-002**: María García.
*   **user-003**: Carlos López.
*   **Categorías**: `c-general` y `c-servicios`.
