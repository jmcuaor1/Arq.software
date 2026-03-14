import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ItemCard from './components/ItemCard';
import ActionModal from './components/ActionModal';
import { fetchProducts, fetchServices, publishProduct, publishService, sendConsultation } from './services/api';

function App() {
    const [productos, setProductos] = useState([]);
    const [servicios, setServicios] = useState([]);
    const [toasts, setToasts] = useState([]);

    // Modal States
    const [activeModal, setActiveModal] = useState(null); // 'product', 'service', 'consultation'
    const [consultationTarget, setConsultationTarget] = useState(null);

    // Form States
    const [formData, setFormData] = useState({});

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const p = await fetchProducts();
            const s = await fetchServices();
            setProductos(p);
            setServicios(s);
        } catch (error) {
            showToast('Error cargando datos del servidor', 'error');
        }
    };

    const showToast = (message, type = 'success') => {
        const id = Date.now();
        setToasts(prev => [...prev, { id, message, type }]);
        setTimeout(() => {
            setToasts(prev => prev.filter(t => t.id !== id));
        }, 5000);
    };

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // Form Submits
    const handleSubmitProduct = async (e) => {
        e.preventDefault();
        try {
            await publishProduct({
                ...formData,
                precio: parseFloat(formData.precio),
                vendedor_status: "APPROVED" // Required by backend
            });
            showToast('✅ Producto publicado exitosamente');
            setActiveModal(null);
            loadData();
        } catch (error) {
            showToast('❌ Ocurrió un error al publicar', 'error');
        }
    };

    const handleSubmitService = async (e) => {
        e.preventDefault();
        try {
            await publishService({
                ...formData,
                precio: parseFloat(formData.precio),
                proveedor_status: "APPROVED" // Required by backend
            });
            showToast('✅ Servicio ofrecido exitosamente');
            setActiveModal(null);
            loadData();
        } catch (error) {
            showToast('❌ Ocurrió un error al ofrecer el servicio', 'error');
        }
    };

    const handleSubmitConsultation = async (e) => {
        e.preventDefault();
        try {
            await sendConsultation({
                comprador_id: formData.comprador_id || 'user-003',
                item_id: consultationTarget.item.id,
                item_type: consultationTarget.type,
                mensaje: formData.mensaje || ''
            });
            showToast('📬 Mensaje enviado exitosamente');
            setActiveModal(null);
        } catch (error) {
            showToast('❌ Error enviando mensaje', 'error');
        }
    };

    // Open Modals Configuration
    const openConsultation = (item, type) => {
        setConsultationTarget({ item, type });
        setFormData({});
        setActiveModal('consultation');
    };

    return (
        <>
            {/* Background Animations */}
            <div className="background-bubbles">
                <div className="bubble"></div>
                <div className="bubble"></div>
                <div className="bubble"></div>
            </div>

            <Navbar 
                onOpenProductModal={() => { setFormData({}); setActiveModal('product'); }} 
                onOpenServiceModal={() => { setFormData({}); setActiveModal('service'); }} 
            />

            <main className="container">
                <h2 style={{marginBottom: '1rem', color: 'var(--text-secondary)'}}>📱 Catálogo de Vecinos</h2>
                <div className="grid">
                    {productos.map(p => <ItemCard key={`p-${p.id}`} item={p} isService={false} onContactClick={openConsultation} />)}
                    {servicios.map(s => <ItemCard key={`s-${s.id}`} item={s} isService={true} onContactClick={openConsultation} />)}
                    {productos.length === 0 && servicios.length === 0 && (
                        <p style={{color: 'var(--text-secondary)', fontStyle: 'italic'}}>Aún no hay publicaciones en la residencia.</p>
                    )}
                </div>
            </main>

            {/* Modals rendered conditionally */}
            <ActionModal 
                isOpen={activeModal === 'product'} 
                onClose={() => setActiveModal(null)}
                title="Publicar Nuevo Producto"
                onSubmit={handleSubmitProduct}
            >
                <label>Vendedor</label>
                <select name="vendedor_id" required onChange={handleInputChange} defaultValue="">
                    <option value="" disabled>Seleccione vendedor...</option>
                    <option value="user-001">Juan Pérez (Apto 101)</option>
                    <option value="user-002">María García (Apto 202)</option>
                </select>

                <label>Nombre del Producto</label>
                <input type="text" name="nombre" placeholder="Ej: Bicicleta Trek..." required onChange={handleInputChange} />

                <label>Precio (COP)</label>
                <input type="number" name="precio" placeholder="150000" min="0" required onChange={handleInputChange} />

                <label>Categoría</label>
                <select name="categoria_id" required onChange={handleInputChange} defaultValue="">
                    <option value="" disabled>Seleccione categoría...</option>
                    <option value="c-general">Categoría General</option>
                </select>

                <label>Descripción</label>
                <textarea name="descripcion" rows="3" placeholder="Detalles de estado, años de uso..." onChange={handleInputChange}></textarea>
                
                <button type="submit" className="btn btn-primary" style={{marginTop: '1rem'}}>Confirmar Publicación</button>
            </ActionModal>

            <ActionModal 
                isOpen={activeModal === 'service'} 
                onClose={() => setActiveModal(null)}
                title="Ofrecer Servicio"
                onSubmit={handleSubmitService}
            >
                <label>Proveedor</label>
                <select name="proveedor_id" required onChange={handleInputChange} defaultValue="">
                    <option value="" disabled>Seleccione proveedor...</option>
                    <option value="user-001">Juan Pérez (Apto 101)</option>
                    <option value="user-002">María García (Apto 202)</option>
                </select>

                <label>Nombre del Servicio</label>
                <input type="text" name="nombre" placeholder="Ej: Paseo de Perros..." required onChange={handleInputChange} />

                <label>Precio (COP)</label>
                <input type="number" name="precio" placeholder="25000" min="0" required onChange={handleInputChange} />

                <label>Categoría</label>
                <select name="categoria_id" required onChange={handleInputChange} defaultValue="">
                    <option value="" disabled>Seleccione categoría...</option>
                    <option value="c-servicios">Servicios Generales</option>
                </select>

                <label>Descripción</label>
                <textarea name="descripcion" rows="3" placeholder="Disponibilidad, herramientas..." onChange={handleInputChange}></textarea>
                
                <button type="submit" className="btn btn-secondary" style={{marginTop: '1rem'}}>Confirmar Servicio</button>
            </ActionModal>

            <ActionModal 
                isOpen={activeModal === 'consultation'} 
                onClose={() => setActiveModal(null)}
                title={`Enviar Consulta sobre: ${consultationTarget?.item?.nombre}`}
                onSubmit={handleSubmitConsultation}
            >
                <label>Soy el interesado:</label>
                <select name="comprador_id" required onChange={handleInputChange} defaultValue="">
                    <option value="" disabled>Seleccione su cuenta...</option>
                    <option value="user-001">Juan Pérez (Apto 101)</option>
                    <option value="user-002">María García (Apto 202)</option>
                    <option value="user-003">Carlos López (Apto 303)</option>
                </select>

                <label>Tu Mesaje Privado:</label>
                <textarea name="mensaje" rows="4" placeholder="Escribe tu mensaje o pregunta..." required onChange={handleInputChange}></textarea>
                
                <button type="submit" className="btn btn-primary" style={{marginTop: '1rem'}}>Enviar Mensaje</button>
            </ActionModal>

            {/* Toast Notifications */}
            <div className="toast-container">
                {toasts.map(toast => (
                    <div key={toast.id} className={`toast ${toast.type}`}>
                        {toast.message}
                    </div>
                ))}
            </div>
        </>
    );
}

export default App;
