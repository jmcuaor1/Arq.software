# VecinoMarket - Arquitectura de Software 2026

VecinoMarket es una plataforma de marketplace disenada específicamente para entornos residenciales. El sistema facilita la interacción entre vecinos, permitiendo la publicación de productos y servicios para establecer un canal de comunicación directo entre compradores y vendedores dentro de la misma comunidad.

## Estado del Proyecto: Sprint 1
Para esta primera entrega, el sistema se centra en el desarrollo del núcleo de negocio y la exposición de una API profesional. 

Es importante notar que el alcance se ajustó para priorizar la conexión entre usuarios. Por lo tanto, el sistema funciona actualmente como un centro de consultas y contacto, omitiendo temporalmente funcionalidades de carrito de compras y transacciones financieras para enfocarse en la robustez de la comunicación.

## Arquitectura y Diseño
El proyecto sigue los principios de la Arquitectura Hexagonal (Puertos y Adaptadores), garantizando que las reglas de negocio sean independientes de la tecnología externa.

### Estructura de Capas
*   **Dominio (marketplace/domain):** Contiene las entidades base y la lógica pura del negocio como Usuario, Producto, Servicio y Consulta.
*   **Aplicación (marketplace/application):** Gestiona los casos de uso mediante servicios y comandos (Service Layer), asegurando que la lógica no se filtre a la interfaz.
*   **Infraestructura (marketplace/infrastructure):** Incluye los adaptadores de persistencia (repositorios in-memory) y la lógica de servicios externos como notificaciones.
*   **Interfaz (marketplace/interface):** Implementada con Django REST Framework, utiliza APIViews y Serializers para gestionar la comunicación con clientes externos.

### Patrones Creacionales
Dando cumplimiento a los requerimientos de la asignatura, se implementaron los siguientes patrones:
*   **Builder Pattern:** Aplicado en la creación de productos para manejar sus validaciones y estados de forma atómica.
*   **Factory Pattern:** Utilizado en el sistema de notificaciones para desacoplar el medio de envío de la lógica de aplicación.

## Documentación Técnica
En la carpeta docs se encuentra la documentación detallada necesaria para la evaluación técnica:
1.  Justificación de arquitectura y visión de escalabilidad.
2.  Diagrama de secuencia de la funcionalidad de registro de consultas.
3.  Mensaje de coordinación de equipo.

## Guía de Instalación y Uso
Para ejecutar el proyecto, se recomienda el uso de un entorno virtual para evitar conflictos de dependencias.

1.  Crear entorno virtual: `python -m venv .venv`
2.  Activar entorno (Windows): `.\.venv\Scripts\activate`
3.  Instalar dependencias: `pip install -r requirements.txt`
4.  Ejecutar demostración integral: `python demo_sprint1_completo.py`

---
**Entregable No. 1**
**Profesor:** Nicolás Ramírez Vélez
**Estudiante:** Kevin Pabón y Juan Miguel Cuao
