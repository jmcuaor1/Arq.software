# Modelo de Dominio y Lógica de Negocio

VecinoMarket sigue los principios de **Arquitectura Hexagonal** y **DDD simplificado**. La capa de dominio es puro Python — sin imports de Django, DRF o Flask.

---

## Entidades (`marketplace/domain/`)

| Entidad | Archivo | Descripción |
|---|---|---|
| `Usuario` | `usuario.py` | Residente de la unidad con teléfono y apartamento |
| `UnidadResidencial` | `unidad_residencial.py` | Conjunto o edificio al que pertenecen los vecinos |
| `Categoria` | `categoria.py` | Clasificación de productos y servicios |
| `Producto` | `producto.py` | Bien material con precio, vendedor y categoría |
| `Servicio` | `servicio.py` | Actividad ofrecida por un vecino |
| `Consulta` | `consulta.py` | Intención de contacto entre comprador y vendedor |

---

## Servicios de Aplicación (`marketplace/application/services.py`)

Cada servicio tiene responsabilidad única y recibe Commands como entrada:

| Servicio | Commands que acepta |
|---|---|
| `UsuarioService` | `CrearUsuarioCommand` |
| `UnidadResidencialService` | `CrearUnidadResidencialCommand` |
| `CategoriaService` | `CrearCategoriaCommand` |
| `PublicacionService` | `PublicarProductoCommand` |
| `ServicioService` | `PublicarServicioCommand` |
| `ConsultaService` | `RegistrarConsultaCommand` |

Flujo interno de cada servicio:
1. Recibe un Command (DTO inmutable).
2. Recupera entidades relacionadas del repositorio.
3. Aplica reglas de negocio (permisos, validaciones de dominio).
4. Persiste el resultado.
5. Dispara notificación si aplica.

---

## Patrón Command

Los Commands son `dataclass` de Python. Garantizan que la capa de aplicación reciba datos estructurados y desacoplados de los Serializers HTTP:

```python
# Ejemplo
@dataclass
class PublicarProductoCommand:
    vendedor_id: str
    nombre: str
    descripcion: str
    precio_cop: float
    categoria_id: str
    imagenes: list = field(default_factory=list)
```

---

## Infraestructura (`marketplace/infrastructure/`)

| Componente | Descripción |
|---|---|
| `InMemory*Repository` | Repositorios en memoria — intercambiables por ORM sin tocar dominio |
| `NotifierFactory` | Retorna un `Notifier` según el canal (actualmente `ConsoleNotifier`) |
| `ConsoleNotifier` | Implementación base — imprime la notificación en consola |

El envío real de notificaciones (SMS, email) fue **extraído al microservicio Flask** mediante el Strangler Pattern y es accesible en `/api/v2/notificaciones/`.

---

## Flujo: Publicar un Producto

```
React (POST /api/productos/)
  → Django View: valida JSON con PublicarProductoSerializer
  → Construye PublicarProductoCommand
  → PublicacionService: verifica vendedor, categoría, permisos
  → ProductoBuilder: construye entidad Producto válida
  → InMemoryProductoRepository.guardar()
  → Respuesta 201 con datos del producto
```

## Flujo: Registrar una Consulta

```
React (POST /api/consultas/)
  → Django View: valida con RegistrarConsultaSerializer
  → Construye RegistrarConsultaCommand
  → ConsultaService: verifica comprador, ítem (producto o servicio)
  → InMemoryConsultaRepository.guardar()
  → Respuesta 201 con datos de la consulta
```
