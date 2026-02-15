# Justificación Arquitectónica y Visión de Escalabilidad

Este documento detalla las razones detrás de la estructura de carpetas actual y cómo esta disposición prepara a **VecinoMarket** para un crecimiento sostenido y una eventual migración a microservicios.

## 1. Justificación de la Estructura (Arquitectura Hexagonal)

Hemos adoptado una estructura basada en Capas de Responsabilidad (Arquitectura Limpia/Hexagonal) para asegurar el desacoplamiento:

*   **`domain/` (Núcleo)**: Contiene la lógica pura de negocio y las entidades (`Producto`, `Servicio`, `Consulta`). Es agnóstica a la base de datos o al framework web.
*   **`application/` (Casos de Uso)**: Contiene los servicios que orquestan el negocio. Aquí es donde se aplican los patrones **Command** y **Service**, permitiendo que la lógica de "Cómo se publica un producto" sea independiente de "Cómo se recibe el HTTP".
*   **`infrastructure/` (Adaptadores)**: Gestiona la persistencia (`repositories.py`) y servicios externos. Actualmente usamos repositorios `InMemory`, pero la estructura permite cambiarlos por PostgreSQL o MongoDB sin tocar una sola línea de lógica de negocio.
*   **`interface/` (Presentación)**: Define cómo el mundo exterior interactúa con nosotros (vía Django REST Framework).

**¿Por qué esta complejidad?**
Para evitar que el código se convierta en un "espagueti" de Django. Si mañana decidimos cambiar Django por FastAPI, el 80% del código (Dominio y Aplicación) permanecerá intacto.

## 2. Preparación para API Gateway y Escalabilidad

El diseño actual está estratégicamente preparado para un entorno de **API Gateway**:

### 1. Controllers Delgados (Thin Controllers)
Nuestras `Views` en `interface/views.py` no tienen lógica de negocio; solo validan el formato y delegan. Un API Gateway puede gestionar la autenticación, el rate limiting y el balanceo de carga antes de que la petición llegue a estos controladores, manteniéndolos ligeros.

### 2. Stateless Services (Servicios sin Estado)
Los servicios en la capa de aplicación no guardan estado local entre peticiones. Toda la información fluye a través de objetos de dominio y se persiste en los repositorios. Esto permite **escalar horizontalmente**: podemos tener 10 instancias del servidor funcionando simultáneamente detrás de un API Gateway y un balanceador de carga.

### 3. Facilidad de Extracción (Microservicios)
La arquitectura está segmentada por módulos claros. Si el volumen de `Consultas` aumenta masivamente, podemos extraer fácilmente la carpeta `domain/consulta.py` y su servicio correspondiente para crear un **Microservicio de Mensajería/Consultas** independiente. El API Gateway simplemente redirigiría el tráfico de `/api/consultas/` hacia ese nuevo servicio sin afectar al resto del sistema.

### 4. Interoperabilidad
Al usar comandos (`RegistrarConsultaCommand`) y serializers estandarizados, el sistema está listo para ser consumido por múltiples frentes (Web, App Móvil, Integraciones de terceros) a través de un punto de entrada único (el Gateway).

---
**Documentación Técnica - VecinoMarket Sprint 1**
