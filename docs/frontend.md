# Documentación del Frontend (React SPA)

El frontend de VecinoMarket ha sido migrado a React para proporcionar una experiencia de usuario rápida y moderna utilizando una estética de **Glassmorphism**.

## Tecnologías Utilizadas
*   **React 18**: Librería base.
*   **Vite**: Herramienta de construcción (build tool) ultra rápida.
*   **Vanilla CSS**: Estilos personalizados sin frameworks pesados.

---

##  Componentes UI
Los componentes se encuentran en `frontend_react/src/components/`:

1.  **Navbar.jsx**: Barra superior con navegación y botones de acción global (+ Publicar).
2.  **ItemCard.jsx**: Tarjeta versátil que muestra tanto Productos como Servicios. Cambia de color dinámicamente según el tipo de ítem.
3.  **ActionModal.jsx**: Modal genérico diseñado para formularios. Se utiliza para publicar productos, ofrecer servicios y enviar consultas.

---

##  Capa de Servicio (Peticiones API)
Toda la comunicación con el servidor ocurre en `frontend_react/src/services/api.js`.

### Funciones Principales:
*   `fetchProducts()`: Obtiene la lista de productos del backend.
*   `publishProduct(data)`: Envía un nuevo producto al servidor (POST).
*   `sendConsultation(data)`: Registra un mensaje de un interesado a un vendedor.

---

##  Diseño Visual: Glassmorphism
El diseño busca una apariencia "premium" mediante el uso de:
*   `backdrop-filter: blur(16px)`: Efecto de cristal esmerilado.
*   `linear-gradient`: Degradados suaves en botones y títulos.
*   `background-bubbles`: Fondo animado con burbujas flotantes definidas en `index.css`.

---

##  Estado de la Aplicación
Usamos el hook `useState` en `App.jsx` para manejar los datos del catálogo en tiempo real. Cuando una petición POST es exitosa, la función `loadData()` se vuelve a ejecutar para refrescar la pantalla sin necesidad de recargar la página.
