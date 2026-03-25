import React, { useState, useEffect, useMemo } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import FilterBar from './components/FilterBar';
import ItemCard from './components/ItemCard';
import EmptyState from './components/EmptyState';
import ActionModal from './components/ActionModal';
import Footer from './components/Footer';
import { fetchProducts, fetchServices, publishProduct, publishService, sendConsultation } from './services/api';

function App() {
    // Data State
    const [productos, setProductos] = useState([]);
    const [servicios, setServicios] = useState([]);
    const [loading, setLoading] = useState(true);

    // Filter State
    const [activeFilter, setActiveFilter] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');

    // Modal State
    const [activeModal, setActiveModal] = useState(null);
    const [consultationTarget, setConsultationTarget] = useState(null);
    const [formData, setFormData] = useState({});

    // Toast State
    const [toasts, setToasts] = useState([]);

    // Load data on mount
    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const [p, s] = await Promise.all([fetchProducts(), fetchServices()]);
            setProductos(p);
            setServicios(s);
        } catch (error) {
            showToast('Error cargando datos del servidor', 'error');
        } finally {
            setLoading(false);
        }
    };

    // Filtered items
    const filteredItems = useMemo(() => {
        let items = [];
        if (activeFilter === 'all' || activeFilter === 'products') {
            items.push(...productos.map(p => ({ ...p, _isService: false })));
        }
        if (activeFilter === 'all' || activeFilter === 'services') {
            items.push(...servicios.map(s => ({ ...s, _isService: true })));
        }
        if (searchQuery.trim()) {
            const q = searchQuery.toLowerCase();
            items = items.filter(i => i.nombre?.toLowerCase().includes(q));
        }
        return items;
    }, [productos, servicios, activeFilter, searchQuery]);

    // Toast system
    const showToast = (message, type = 'success') => {
        const id = Date.now();
        setToasts(prev => [...prev, { id, message, type }]);
        setTimeout(() => {
            setToasts(prev => prev.filter(t => t.id !== id));
        }, 4000);
    };

    // Form handling
    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const openModal = (type, target = null) => {
        setFormData({});
        setConsultationTarget(target);
        setActiveModal(type);
    };

    const closeModal = () => setActiveModal(null);

    // Submit handlers
    const handleSubmitProduct = async (e) => {
        e.preventDefault();
        try {
            await publishProduct({
                ...formData,
                precio: parseFloat(formData.precio),
                vendedor_status: 'APPROVED',
            });
            showToast('✅ Producto publicado exitosamente');
            closeModal();
            loadData();
        } catch {
            showToast('❌ Error al publicar el producto', 'error');
        }
    };

    const handleSubmitService = async (e) => {
        e.preventDefault();
        try {
            await publishService({
                ...formData,
                precio: parseFloat(formData.precio),
                proveedor_status: 'APPROVED',
            });
            showToast('✅ Servicio ofrecido exitosamente');
            closeModal();
            loadData();
        } catch {
            showToast('❌ Error al ofrecer el servicio', 'error');
        }
    };

    const handleSubmitConsultation = async (e) => {
        e.preventDefault();
        try {
            await sendConsultation({
                comprador_id: formData.comprador_id || 'user-003',
                item_id: consultationTarget.item.id,
                item_type: consultationTarget.type,
                mensaje: formData.mensaje || '',
            });
            showToast('📬 Mensaje enviado exitosamente');
            closeModal();
        } catch {
            showToast('❌ Error enviando mensaje', 'error');
        }
    };

    const handleContactClick = (item, type) => {
        openModal('consultation', { item, type });
    };

    const scrollToCatalog = () => {
        document.getElementById('catalogo')?.scrollIntoView({ behavior: 'smooth' });
    };

    // Skeleton cards for loading
    const renderSkeletons = () => (
        Array.from({ length: 6 }).map((_, i) => (
            <div className="skeleton-card" key={`sk-${i}`}>
                <div className="skeleton-line w-40"></div>
                <div className="skeleton-line w-80 h-6"></div>
                <div className="skeleton-line w-full"></div>
                <div className="skeleton-line w-60"></div>
                <div className="skeleton-line w-40 h-8"></div>
                <div className="skeleton-line w-full h-10"></div>
            </div>
        ))
    );

    return (
        <>
            {/* Background Decoration */}
            <div className="background-orbs" aria-hidden="true">
                <div className="orb"></div>
                <div className="orb"></div>
                <div className="orb"></div>
            </div>

            {/* Navigation */}
            <Navbar
                onOpenProductModal={() => openModal('product')}
                onOpenServiceModal={() => openModal('service')}
            />

            {/* Hero */}
            <HeroSection
                productCount={productos.length}
                serviceCount={servicios.length}
                onExplore={scrollToCatalog}
                onPublish={() => openModal('product')}
            />

            {/* Main Content */}
            <main className="container">
                <FilterBar
                    activeFilter={activeFilter}
                    onFilterChange={setActiveFilter}
                    searchQuery={searchQuery}
                    onSearchChange={setSearchQuery}
                    resultCount={filteredItems.length}
                />

                <div className="grid">
                    {loading ? (
                        renderSkeletons()
                    ) : filteredItems.length > 0 ? (
                        filteredItems.map(item => (
                            <ItemCard
                                key={`${item._isService ? 's' : 'p'}-${item.id}`}
                                item={item}
                                isService={item._isService}
                                onContactClick={handleContactClick}
                            />
                        ))
                    ) : (
                        <EmptyState
                            onPublishProduct={() => openModal('product')}
                            onPublishService={() => openModal('service')}
                        />
                    )}
                </div>
            </main>

            {/* Footer */}
            <Footer />

            {/* ===== MODALS ===== */}

            {/* Publish Product */}
            <ActionModal
                isOpen={activeModal === 'product'}
                onClose={closeModal}
                title="Publicar Producto"
                subtitle="Comparte algo con tus vecinos"
                onSubmit={handleSubmitProduct}
            >
                <div className="form-group">
                    <label className="form-label">Vendedor</label>
                    <select name="vendedor_id" required onChange={handleInputChange} defaultValue="" className="form-select">
                        <option value="" disabled>Seleccione vendedor...</option>
                        <option value="user-001">Juan Pérez (Apto 101)</option>
                        <option value="user-002">María García (Apto 202)</option>
                    </select>
                </div>
                <div className="form-group">
                    <label className="form-label">Nombre del Producto</label>
                    <input type="text" name="nombre" placeholder="Ej: Bicicleta Trek..." required onChange={handleInputChange} className="form-input" />
                </div>
                <div className="form-group">
                    <label className="form-label">Precio (COP)</label>
                    <input type="number" name="precio" placeholder="150000" min="0" required onChange={handleInputChange} className="form-input" />
                </div>
                <div className="form-group">
                    <label className="form-label">Categoría</label>
                    <select name="categoria_id" required onChange={handleInputChange} defaultValue="" className="form-select">
                        <option value="" disabled>Seleccione categoría...</option>
                        <option value="c-general">Categoría General</option>
                    </select>
                </div>
                <div className="form-group">
                    <label className="form-label">Descripción</label>
                    <textarea name="descripcion" rows="3" placeholder="Detalles de estado, años de uso..." onChange={handleInputChange} className="form-textarea"></textarea>
                </div>
            </ActionModal>

            {/* Offer Service */}
            <ActionModal
                isOpen={activeModal === 'service'}
                onClose={closeModal}
                title="Ofrecer Servicio"
                subtitle="Ofrece tus habilidades a la comunidad"
                onSubmit={handleSubmitService}
            >
                <div className="form-group">
                    <label className="form-label">Proveedor</label>
                    <select name="proveedor_id" required onChange={handleInputChange} defaultValue="" className="form-select">
                        <option value="" disabled>Seleccione proveedor...</option>
                        <option value="user-001">Juan Pérez (Apto 101)</option>
                        <option value="user-002">María García (Apto 202)</option>
                    </select>
                </div>
                <div className="form-group">
                    <label className="form-label">Nombre del Servicio</label>
                    <input type="text" name="nombre" placeholder="Ej: Paseo de Perros..." required onChange={handleInputChange} className="form-input" />
                </div>
                <div className="form-group">
                    <label className="form-label">Precio (COP)</label>
                    <input type="number" name="precio" placeholder="25000" min="0" required onChange={handleInputChange} className="form-input" />
                </div>
                <div className="form-group">
                    <label className="form-label">Categoría</label>
                    <select name="categoria_id" required onChange={handleInputChange} defaultValue="" className="form-select">
                        <option value="" disabled>Seleccione categoría...</option>
                        <option value="c-servicios">Servicios Generales</option>
                    </select>
                </div>
                <div className="form-group">
                    <label className="form-label">Descripción</label>
                    <textarea name="descripcion" rows="3" placeholder="Disponibilidad, herramientas..." onChange={handleInputChange} className="form-textarea"></textarea>
                </div>
            </ActionModal>

            {/* Send Consultation */}
            <ActionModal
                isOpen={activeModal === 'consultation'}
                onClose={closeModal}
                title={`Contactar — ${consultationTarget?.item?.nombre || ''}`}
                subtitle="Envía un mensaje privado al publicador"
                onSubmit={handleSubmitConsultation}
            >
                <div className="form-group">
                    <label className="form-label">Soy el interesado:</label>
                    <select name="comprador_id" required onChange={handleInputChange} defaultValue="" className="form-select">
                        <option value="" disabled>Seleccione su cuenta...</option>
                        <option value="user-001">Juan Pérez (Apto 101)</option>
                        <option value="user-002">María García (Apto 202)</option>
                        <option value="user-003">Carlos López (Apto 303)</option>
                    </select>
                </div>
                <div className="form-group">
                    <label className="form-label">Tu Mensaje Privado:</label>
                    <textarea name="mensaje" rows="4" placeholder="Escribe tu mensaje o pregunta..." required onChange={handleInputChange} className="form-textarea"></textarea>
                </div>
            </ActionModal>

            {/* Toast Notifications */}
            <div className="toast-container" aria-live="polite">
                {toasts.map(toast => (
                    <div key={toast.id} className={`toast ${toast.type}`} role="alert">
                        {toast.message}
                    </div>
                ))}
            </div>
        </>
    );
}

export default App;
