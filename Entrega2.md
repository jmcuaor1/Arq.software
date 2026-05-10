Proyecto de Curso: Arquitectura de Software 2026
Entrega No. 2: Migración a Microservicios, Integración y
Resiliencia
Prof. Nicolás Ram ́ırez V ́elez
Semestre 2026-I
Alineacion ABET (Acreditaci on Internacional)
Resultado del Programa: Desarrolla una solucion final que satisface todos los reque-
rimientos y restricciones identificadas al formular el problema de diseno.
Resultado de la Asignatura: Implementa la arquitectura de software apropiada
(cliente-servidor, por capas, MVC, orientadas a servicios y orientadas a microservicios).

1. Objetivo de la Entrega
   Evolucionar la arquitectura monolítica de la primera entrega hacia un ecosistema hıbrido y
   resiliente desplegado en AWS Academy. Los equipos aplicanran el Strangler Pattern para
   extraer funcionalidades a microservicios, orquestaran el trafico mediante un API Gateway
   (Nginx), e implementar ́una comunicación asıncrona garantizando estandares de usabilidad e
   internacionalización.

2. Requerimientos Técnicos (Grado Empresarial)
   2.1. 1. Despliegue e Infraestructura (Academia AWS)
   Todo el ecosistema (Django, Flask, Nginx, Base de Datos, Message Broker) debe estar
   empaquetado y orquestado con Docker Compose.
   El sistema debe desplegarse en una instancia EC2 de AWS Academy.
   2.2. 2. Arquitectura y Patrón Estrangulador
   A ́ısle funcionalidades del monolito (Django) y mıgrelas a microservicios independientes
   (Flask).
   Configure Nginx como API Gateway para el ruteo de tr ́afico profesional.
   2.3. 3. Integración y Patrones Estructurales
   Servicio a Proveer: Exponga un endpoint JSON con informacion relevante del sistema.
   Servicio a Consumir: Consuma el servicio del equipo aliado y mu ́estrelo en su aplicaci ́on.
   API de Terceros: Consumo obligatorio mediante el Patr ́on Adapter (Inversion de
   Dependencias).
   1
   2.4. 4. Comunicacin Asıncrona e i18n
   Eventos: Uso de Message Broker (Redis/Celery) para procesos de fondo (reportes, noti-
   ficaciones).
   Usabilidad: Auditorıa de UI/UX, navegacion y formularios robustos.
   i18n: Soporte bilingue completo mediante gettext. Prohibido el uso de textos quemados.
3. R ​​́ubrica de Evaluacin Institucional (ABET)
   ADVERTENCIA CRITICA
   De acuerdo con los lineamientos del curso: Si el equipo no realiza el 100 % de las
   correcciones notificadas en la Entrega 1, la nueva entrega NO ser ́a revisada y
   la nota ser ́a 0.0.
   Criterio Descripcion Peso
   Correcciones E1 Implementacion total de ajustes indicados en la sustentaci ́on
   previa.
   10 %
   Arquitectura Actualizacion de diagramas incluyendo AWS, Nginx, Flask y
   Broker.
   10 %
   Servicios Exposicion de API, consumo de aliado y consumo de tercero v ́ıa
   Adapter.
   30 %
   Infraestructura Despliegue en AWS Academy con Docker y ruteo v ́ıa Nginx
   Gateway.
   30 %
   Resiliencia y UX Implementacion de i18n, usabilidad y tareas as ́ıncronas as ́ıncro-
   nas.
   20 %
   Cuadro 1: Matriz de Evaluacion - Entregable 2
4. Bono de Excelencia Arquitectonica
   Exenci ́on de Parcial 02
   Aquellos equipos que logren llevar su arquitectura mas alla del requerimiento mınimo
   y migren mas del 70 % de sus servicios y logica de negocio a microservicios
   funcionales e independientes, quedaran automaticamente eximidos de presentar
   el Parcial 02 de la asignatura.
5. Instrucciones de Entrega
   Comparte el enlace del repositorio (rama principal) y la IP el ́astica de AWS en la plataforma
   institucional.
   Evidencia de Trabajo: Estudiante sin commits en el repositorio tiene nota de 0.0.
   La instancia de AWS EC2 debe estar encendida para la sustentación.
