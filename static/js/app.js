document.addEventListener('DOMContentLoaded', () => {
    // API Endpoints
    const API = {
        productos: '/api/publicar-producto/',
        productosList: '/api/productos/',
        servicios: '/api/servicios/',
        consultas: '/api/consultas/'
    };

    // DOM Elements
    const grid = document.getElementById('contentGrid');
    const toastContainer = document.getElementById('toastContainer');
    
    // Buttons
    const btnProductos = document.getElementById('btnProductos');
    const btnServicios = document.getElementById('btnServicios');
    const btnConsultas = document.getElementById('btnConsultas');
    const btnNuevoProducto = document.getElementById('btnNuevoProducto');
    const btnNuevoServicio = document.getElementById('btnNuevoServicio');

    // Modals
    const modalProducto = document.getElementById('modalProducto');
    const modalServicio = document.getElementById('modalServicio');
    const modalConsulta = document.getElementById('modalConsulta');
    const closeBtns = document.querySelectorAll('.close-btn');

    // Default current user (for demo purposes)
    const CURRENT_USER_ID = "user-001";
    
    // --- State ---
    let currentView = 'productos'; // 'productos' | 'servicios' | 'consultas'
    let lastCreatedItemId = 'dummy-item-123';

    // --- Helpers ---
    const showToast = (msg, type = 'success') => {
        const t = document.createElement('div');
        t.className = `toast ${type}`;
        t.innerHTML = `<strong>${type === 'success' ? '✅' : '❌'}</strong> ${msg}`;
        toastContainer.appendChild(t);
        setTimeout(() => t.remove(), 4000);
    };

    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    const csrftoken = getCookie('csrftoken');

    // --- Data Fetching ---
    // Since our backend doesn't have list endpoints yet for everything except 'consultas', 
    // we'll mock the listing for the frontend to show something. 
    // In a real scenario, we would add GET /api/productos/ endpoints.
    
    // Let's create an initial dummy product and service via API if we haven't
    const initDummyData = async () => {
        try {
            // Check if backend responds
            const res = await fetch('/api/usuarios/');
            if(res.ok) {
                console.log("Backend en linea.");
            }
        } catch(e) {
            console.error("Error connecting to backend", e);
        }
    };

    const loadData = async (type) => {
        grid.innerHTML = '<div class="loading">Cargando...</div>';
        currentView = type;
        
        btnProductos.classList.toggle('active', type === 'productos');
        btnServicios.classList.toggle('active', type === 'servicios');
        btnConsultas.classList.toggle('active', type === 'consultas');

        if(type === 'consultas') {
            try {
                // To fetch consultas, we need a GET endpoint. Our ConsultaView supports GET?
                const response = await fetch(`${API.consultas}?vendedor_id=${CURRENT_USER_ID}`);
                if(!response.ok) throw new Error("No pudimos cargar consultas.");
                const data = await response.json();
                
                grid.innerHTML = '';
                if(data.length === 0) {
                    grid.innerHTML = '<div class="desc">No tienes consultas activas en este momento.</div>';
                    return;
                }

                data.forEach(c => {
                    const el = document.createElement('div');
                    el.className = 'card glass-panel';
                    el.innerHTML = `
                        <h3>Interés en: ${c.item_nombre}</h3>
                        <div class="meta">De: ${c.comprador_nombre}</div>
                        <div class="meta">Estado: ${c.estado}</div>
                        <p class="desc"><b>Mensaje:</b> ${c.mensaje || 'Sin mensaje'}</p>
                    `;
                    grid.appendChild(el);
                });
            } catch(e) {
                grid.innerHTML = `<div class="desc" style="color:red">Error: ${e.message}</div>`;
            }
        } else if (type === 'productos') {
            try {
                const response = await fetch(API.productosList);
                if(!response.ok) throw new Error("No pudimos cargar productos.");
                const data = await response.json();
                grid.innerHTML = '';
                if(data.length === 0) {
                    grid.innerHTML = '<div class="desc">No hay productos disponibles en este momento.</div>';
                    return;
                }
                data.forEach(p => {
                    const el = document.createElement('div');
                    el.className = 'card glass-panel';
                    el.innerHTML = `
                        <h3>${p.nombre}</h3>
                        <div class="meta">💰 $${p.precio} | 📁 ${p.categoria_nombre}</div>
                        <div class="meta">Vendedor ID: ${p.vendedor_id}</div>
                        <p class="desc">${p.descripcion || 'Sin descripción'}</p>
                        <button class="btn btn-primary w-100" onclick="openConsultaModal('${p.id}', 'producto')" style="margin-top:1rem;">
                            Contactar Vendedor
                        </button>
                    `;
                    grid.appendChild(el);
                });
            } catch(e) {
                grid.innerHTML = `<div class="desc" style="color:red">Error: ${e.message}</div>`;
            }
        } else if (type === 'servicios') {
            try {
                const response = await fetch(API.servicios);
                if(!response.ok) throw new Error("No pudimos cargar servicios.");
                const data = await response.json();
                grid.innerHTML = '';
                if(data.length === 0) {
                    grid.innerHTML = '<div class="desc">No hay servicios disponibles en este momento.</div>';
                    return;
                }
                data.forEach(s => {
                    const el = document.createElement('div');
                    el.className = 'card glass-panel';
                    el.innerHTML = `
                        <h3>${s.nombre}</h3>
                        <div class="meta">💰 Base: $${s.precio} | 📁 ${s.categoria_nombre}</div>
                        <div class="meta">Proveedor ID: ${s.proveedor_id}</div>
                        <p class="desc">${s.descripcion || 'Sin descripción'}</p>
                        <button class="btn btn-secondary w-100" onclick="openConsultaModal('${s.id}', 'servicio')" style="margin-top:1rem;">
                            Contactar Proveedor
                        </button>
                    `;
                    grid.appendChild(el);
                });
            } catch(e) {
                grid.innerHTML = `<div class="desc" style="color:red">Error: ${e.message}</div>`;
            }
        }
    };

    // --- Modal Logic ---
    window.openConsultaModal = (itemId, itemType) => {
        document.getElementById('consultaItemId').value = itemId;
        document.getElementById('consultaItemType').value = itemType;
        modalConsulta.classList.add('show');
    };

    btnNuevoProducto.onclick = () => modalProducto.classList.add('show');
    btnNuevoServicio.onclick = () => modalServicio.classList.add('show');
    
    closeBtns.forEach(btn => {
        btn.onclick = (e) => {
            e.target.closest('.modal').classList.remove('show');
        };
    });

    window.onclick = (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('show');
        }
    };

    // --- Forms ---
    document.getElementById('formProducto').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            nombre: document.getElementById('prodNombre').value,
            precio: parseFloat(document.getElementById('prodPrecio').value),
            descripcion: document.getElementById('prodDesc').value,
            categoria_id: document.getElementById('prodCategoria').value,
            vendedor_id: document.getElementById('prodVendedor').value,
            vendedor_status: "APPROVED",
            imagenes: ["http://ejemplo.com/default.png"]
        };

        try {
            const res = await fetch(API.productos, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            });
            const responseData = await res.json();
            if(res.ok) {
                lastCreatedItemId = responseData.id;
                showToast("Producto creado exitosamente!");
                modalProducto.classList.remove('show');
                loadData('productos');
            } else {
                showToast(JSON.stringify(responseData), 'error');
            }
        } catch(e) {
            showToast("Error de conexión", 'error');
        }
    });

    document.getElementById('formServicio').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            nombre: document.getElementById('servNombre').value,
            precio: parseFloat(document.getElementById('servPrecio').value),
            descripcion: document.getElementById('servDesc').value,
            categoria_id: document.getElementById('servCategoria').value,
            proveedor_id: document.getElementById('servProveedor').value,
            proveedor_status: "APPROVED"
        };

        try {
            const res = await fetch(API.servicios, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            });
            const responseData = await res.json();
            if(res.ok) {
                lastCreatedItemId = responseData.id;
                showToast("Servicio orfrecido exitosamente!");
                modalServicio.classList.remove('show');
                loadData('servicios');
            } else {
                showToast(JSON.stringify(responseData), 'error');
            }
        } catch(e) {
            showToast("Error de conexión", 'error');
        }
    });

    document.getElementById('formConsulta').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            comprador_id: document.getElementById('consultaCompradorId').value,
            comprador_status: "APPROVED",
            item_id: document.getElementById('consultaItemId').value,
            item_type: document.getElementById('consultaItemType').value,
            mensaje: document.getElementById('consultaMensaje').value
        };

        try {
            const res = await fetch(API.consultas, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            });
            eventData = await res.json();
            if(res.ok) {
                showToast("Consulta enviada. Revisa el terminal del servidor.");
                modalConsulta.classList.remove('show');
            } else {
                showToast(JSON.stringify(eventData), 'error');
            }
        } catch(e) {
            showToast("Error de conexión", 'error');
        }
    });

    // --- Initialization ---
    btnProductos.onclick = () => loadData('productos');
    btnServicios.onclick = () => loadData('servicios');
    btnConsultas.onclick = () => loadData('consultas');

    initDummyData();
    loadData('productos');
});
