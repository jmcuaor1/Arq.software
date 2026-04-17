# Documentación del Backend

El backend está dividido en dos servicios: el **monolito Django** (dominio central) y el **microservicio Flask** de notificaciones (Strangler Pattern).

---

## Monolito Django — `/api/v1/`

### Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `GET/POST` | `/api/usuarios/` | Listar / crear usuarios |
| `GET/POST` | `/api/unidades/` | Listar / crear unidades residenciales |
| `GET/POST` | `/api/categorias/` | Listar / crear categorías |
| `GET/POST` | `/api/productos/` | Listar / publicar productos |
| `GET/POST` | `/api/servicios/` | Listar / publicar servicios |
| `POST` | `/api/consultas/` | Registrar consulta de contacto |
| `GET` | `/api/consultas/?vendedor_id=X` | Consultas por vendedor |
| `GET` | `/api/consultas/?comprador_id=X` | Consultas por comprador |

Vía Nginx, estas rutas son accesibles como `/api/v1/productos/`, `/api/v1/servicios/`, etc.

### Mapeo de errores HTTP

| Excepción de dominio | Código HTTP |
|---|---|
| `DomainError` / `ValidationError` | 400 |
| `PermissionError` | 403 |
| `ResourceNotFoundError` | 404 |
| `ResourceAlreadyExistsError` | 409 |
| Error inesperado | 500 |

### Capas (Thin Controllers)

`views.py` solo hace tres cosas: validar con Serializer → construir Command → delegar al Service. No contiene lógica de negocio.

### Datos de prueba (cargados al iniciar)

| ID | Nombre | Email |
|---|---|---|
| user-001 | Juan Pérez | juan@test.com |
| user-002 | María García | mariag@test.com |
| user-003 | Carlos López | carlos@test.com |

Categorías: `c-general` (General), `c-servicios` (Servicios).

---

## Microservicio Flask — `/api/v2/notificaciones/`

Módulo extraído del monolito mediante el **Strangler Pattern**. Gestiona el envío de notificaciones de forma independiente.

### Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/v2/notificaciones/` | Lista canales disponibles |
| `POST` | `/api/v2/notificaciones/` | Envía una notificación |

### Ejemplo POST

**Request:**
```json
{
  "telefono": "3001234567",
  "titulo": "Tu publicación fue creada",
  "tipo": "sms"
}
```

**Respuesta 201:**
```json
{
  "estado": "enviado",
  "canal": "sms",
  "destinatario": "3001234567",
  "titulo": "Tu publicación fue creada"
}
```

**Respuesta 400 (validación):**
```json
{
  "error": "Datos inválidos",
  "detalle": {
    "tipo": "Tipo inválido. Opciones válidas: email, sms, consola."
  }
}
```

Tipos válidos: `email`, `sms`, `consola`.
