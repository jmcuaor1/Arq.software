# Diagrama de Secuencia: Registro de Consulta

Este diagrama describe el flujo de interaccio´n entre las capas del sistema (Arquitectura Hexagonal) incorporando patrones creacionales segu´n la ru´brica.

```mermaid
sequenceDiagram
    participant Cliente as Cliente (Postman/Web)
    participant View as ConsultaView (Interface)
    participant Serializer as RegistrarConsultaSerializer
    participant Service as ConsultaService (Application)
    participant Factory as NotifierFactory (Infra)
    participant Repo as InMemoryConsultaRepository (Infra)
    participant Domain as Consulta (Domain Entity)

    Note over Cliente, Domain: Flujo de Registro de Intere´s (Patrones Factory Incluido)

    Cliente->>View: POST /api/consultas/ (JSON)
    View->>Serializer: is_valid(data)
    Serializer-->>View: Validado (OK)
    
    View->>Service: registrar_consulta(Command)
    
    Service->>Repo: Validar Existencia Item/Usuario
    Repo-->>Service: Datos Obtenidos
    
    Service->>Domain: Instanciar Entidad Consulta
    Domain-->>Service: Objeto Consulta
    
    Service->>Repo: add(consulta)
    Repo-->>Service: Guardado exitoso

    %% Aplicacio´n de Patro´n Factory exigido por Ru´brica
    Service->>Factory: create()
    Factory-->>Service: Notificador (ConsoleNotifier)
    Service->>Service: notify("Nuevo interesado")
    
    Service-->>View: Entidad Consulta Creada
    View-->>Cliente: HTTP 201 Created (JSON Resumen)
```

## Justificacio´n de Patrones Creacionales
1. **Factory Method (NotifierFactory)**: Se utiliza para desacoplar la lo´gica de negocio del medio de comunicacio´n (Consola, WhatsApp, Email). Cumple con el requerimiento de gestionar una dependencia externa.
2. **Builder Pattern (ProductoBuilder)**: Aunque no se muestra en este diagrama simple, el sistema utiliza un Builder para la entidad `Producto` (localizado en `builders.py`), garantizando que la creacio´n de la clase ma´s compleja del dominio sea at´omica y validada.

## Estructura de Capas
- **Interface**: `ConsultaView` y `RegistrarConsultaSerializer`.
- **Application**: `ConsultaService` (Orquestador).
- **Domain**: Entidad `Consulta` (Lo´gica pura).
- **Infrastructure**: Repositorios y Notificadores.
