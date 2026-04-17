# Documentación del Frontend (React SPA)

Frontend de VecinoMarket construido con React 19.2 y Vite 8. Implementa un **dark theme premium** con design system propio basado en CSS custom properties.

## Tecnologías

- **React 19.2** — Librería de UI
- **Vite 8** — Build tool y dev server (HMR)
- **Vanilla CSS** — Design system con 80+ tokens en `index.css`

---

## Componentes

Ubicados en `frontend_react/src/components/`:

| Componente | Responsabilidad |
|---|---|
| `HeroSection.jsx` | Landing con propuesta de valor, estadísticas y CTAs |
| `FilterBar.jsx` | Tabs (Todo / Productos / Servicios), búsqueda por texto y contador de resultados |
| `ItemCard.jsx` | Tarjeta de producto o servicio con avatar, badge de tipo y precio con gradiente |
| `ActionModal.jsx` | Diálogo ARIA con focus trap y cierre por Escape — usado para publicar y consultar |
| `EmptyState.jsx` | Estado vacío con CTA para la primera publicación |
| `Navbar.jsx` | Barra de navegación con logo y ARIA labels |
| `Footer.jsx` | Pie de página con branding |

---

## Estado de la Aplicación (`App.jsx`)

- Fetching paralelo con `Promise.all([fetchProducts(), fetchServices()])` al montar.
- Filtrado por tipo y término de búsqueda con `useMemo` — sin re-fetching al escribir.
- Skeleton loading mientras llegan los datos del backend.

---

## Capa de Servicios (`services/api.js`)

Todas las llamadas HTTP están centralizadas aquí. Los componentes nunca usan `fetch()` directamente.

| Función | Método | Endpoint |
|---|---|---|
| `fetchProducts()` | GET | `/api/productos/` |
| `fetchServices()` | GET | `/api/servicios/` |
| `publishProduct(data)` | POST | `/api/productos/` |
| `publishService(data)` | POST | `/api/servicios/` |

La URL base apunta a `http://127.0.0.1:8000/api` en desarrollo local. Con Docker, el tráfico pasa por Nginx en el puerto 8080.

---

## Design System

El tema oscuro está definido en `index.css` mediante CSS custom properties (`--color-*`, `--spacing-*`, `--radius-*`). No usar colores o espaciados hardcodeados en componentes — siempre referenciar los tokens.
