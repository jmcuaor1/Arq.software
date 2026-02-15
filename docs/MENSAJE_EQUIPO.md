# Nota para el Equipo: Ajuste de Alcance (Sprint 1)

Oe Cuao,

 Dejo este mensaje con IA que explica el cambio de alcance del sprint 1 y las modificaciones que hice. el otro archivo es md es La wiki tecnica que pide la sección 3 del entregable falta solo el diagrama de secuencia.

### ¿Qué cambió?
Hemos decidido que el marketplace funcione exclusivamente como un **punto de contacto directo** entre vecinos. Por lo tanto, he procedido a:

1.  **Simplificar el Sistema**: Eliminé toda la lógica relacionada con **Carritos de Compra** y **Transacciones** (pagos, totales, estados de confirmación de compra). Esto reduce el riesgo técnico y legal al no manejar dinero directamente en esta fase.
2.  **Nuevo Sistema de Consultas**: En su lugar, implementé una entidad llamada `Consulta`. Ahora, cuando un vecino está interesado en un producto o servicio, simplemente registra una "Consulta" con un mensaje.
3.  **Flujo de Usuario**:
    *   **Comprador**: Ve algo que le gusta -> Envía consulta.
    *   **Vendedor**: Recibe la consulta -> Se pone en contacto fuera del sistema (ej. WhatsApp/Presencial).

### Impacto en el Código
*   **Domino**: Se eliminaron `transaccion.py` y `carrito.py`. Se agregó `consulta.py`.
*   **Servicios**: Desapareció `TransaccionService` y nació `ConsultaService`.
*   **API**: Los endpoints de transacciones fueron reemplazados por `/api/consultas/`.

### ¿Cómo probarlo?
Actualicé el script `demo_sprint1_completo.py`. Si lo ejecutas, verás el nuevo flujo de "Registro de Interés" funcionando de punta a punta.

Cualquier duda sobre la implementación técnica o la nueva estructura, quedó atento para que lo revisemos juntos. ¡Sigamos adelante con el Sprint 2!

Atentamente,
**Kevin**
