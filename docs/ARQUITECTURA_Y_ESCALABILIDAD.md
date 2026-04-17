# Arquitectura y Escalabilidad

## 1. Justificación de la Arquitectura Hexagonal

La capa de dominio (`marketplace/domain/`) es puro Python — cero imports de Django, DRF o cualquier framework. Esto garantiza que si mañana se reemplaza Django por FastAPI, el 80% del código (dominio + aplicación) permanece intacto.

Las capas siguen una dependencia unidireccional estricta:

```
domain/ ← application/ ← infrastructure/ ← interface/
```

Ninguna capa interna conoce a las capas externas. Las Views (`interface/`) son thin controllers: validar → construir Command → delegar. La lógica nunca sube a los controladores.

---

## 2. Strangler Pattern — Migración Progresiva a Microservicios

En el Taller 02 se aplicó el **Strangler Fig Pattern** para extraer el módulo de Notificaciones del monolito Django a un microservicio Flask independiente.

### Por qué Notificaciones fue el candidato

- **Alta frecuencia de cambio**: requiere agregar canales (WhatsApp, push, email) con dependencias externas distintas y ciclos de despliegue independientes.
- **Potencial de bloqueo**: las llamadas a APIs externas (Twilio, SendGrid) tienen latencia variable; correrlas en el hilo de Django degrada todas las demás peticiones.
- **Bajo acoplamiento**: ya estaba aislado detrás de una interfaz `Notifier` y una `NotifierFactory` — la extracción no rompió ningún contrato de dominio.

### Ruteo (Nginx)

```
/api/v2/notificaciones/  →  Flask :5000   (módulo estrangulado)
/api/v1/*                →  Django :8000  (monolito legacy)
```

El monolito no sabe que `/api/v2/notificaciones/` existe. Nginx intercepta el tráfico antes de que llegue a Django.

---

## 3. Preparación para Escalabilidad

### Thin Controllers

Las Views no tienen lógica de negocio. Un API Gateway puede agregar autenticación, rate limiting y balanceo de carga antes de que la petición llegue a los controladores.

### Servicios sin Estado (Stateless)

Los servicios de aplicación no guardan estado local entre peticiones. Esto permite **escalar horizontalmente**: múltiples instancias de Django o Flask detrás de un balanceador sin coordinación de sesión.

### Repositorios Intercambiables

Los repositorios `InMemory*` implementan la misma interfaz que implementaría un repositorio con PostgreSQL. Migrar a base de datos real = crear `DjangoORM*Repository` e inyectarlo en `views.py`. El dominio y la aplicación no cambian.

### Próximos módulos candidatos a estrangular

| Módulo | Razón |
|---|---|
| Consultas / Mensajería | Alto volumen esperado; podría tener su propia cola de mensajes |
| Búsqueda / Catálogo | Puede necesitar Elasticsearch independiente del modelo relacional |

---

## 4. Interoperabilidad

El uso de Commands estandarizados y serializers DRF deja el sistema listo para ser consumido por múltiples clientes (web, móvil, integraciones terceros) a través de un único punto de entrada (Nginx / API Gateway futuro).
