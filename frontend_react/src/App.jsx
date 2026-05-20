import React, { useState, useEffect, useMemo, useCallback } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import FilterBar from './components/FilterBar';
import ItemCard from './components/ItemCard';
import EmptyState from './components/EmptyState';
import ActionModal from './components/ActionModal';
import Footer from './components/Footer';
import {
    fetchProducts,
    fetchServices,
    fetchCategories,
    publishProduct,
    publishService,
    sendConsultation,
    fetchAlliedData,
} from './services/api';
import ProductForm from './components/ProductForm';
import ServiceForm from './components/ServiceForm';

// i18n básico (sin dependencia externa)
const TRANSLATIONS = {
    es: {
        publishProduct: 'Publicar Producto',
        publishService: 'Ofrecer Servicio',
        shareWithNeighbors: 'Comparte algo con tus vecinos',
        offerSkills: 'Ofrece tus habilidades a la comunidad',
        contact: 'Contactar',
        privateMessage: 'Envía un mensaje privado al publicador',
        confirm: 'Confirmar',
        processing: 'Procesando...',
        productPublished: 'Producto publicado exitosamente',
        servicePublished: 'Servicio ofrecido exitosamente',
        messageSent: 'Mensaje enviado exitosamente',
        errorProduct: 'Error al publicar el producto',
        errorService: 'Error al ofrecer el servicio',
        errorMessage: 'Error enviando mensaje',
        loadingError: 'Error cargando datos del servidor',
        alliedData: 'Datos del Equipo Aliado',
        alliedUnavailable: 'El servicio aliado no está disponible en este momento.',
        generateAI: '✨ Generar con IA',
        generatingAI: 'Generando...',
        seller: 'Vendedor',
        provider: 'Proveedor',
        productName: 'Nombre del Producto',
        serviceName: 'Nombre del Servicio',
        price: 'Precio (COP)',
        category: 'Categoría',
        description: 'Descripción',
        iAmInterested: 'Soy el interesado:',
        privateMsg: 'Tu Mensaje Privado:',
    },
    en: {
        publishProduct: 'Publish Product',
        publishService: 'Offer Service',
        shareWithNeighbors: 'Share something with your neighbors',
        offerSkills: 'Offer your skills to the community',
        contact: 'Contact',
        privateMessage: 'Send a private message to the publisher',
        confirm: 'Confirm',
        processing: 'Processing...',
        productPublished: 'Product published successfully',
        servicePublished: 'Service offered successfully',
        messageSent: 'Message sent successfully',
        errorProduct: 'Error publishing the product',
        errorService: 'Error offering the service',
        errorMessage: 'Error sending message',
        loadingError: 'Error loading data from server',
        alliedData: 'Allied Team Data',
        alliedUnavailable: 'The allied service is not available at this time.',
        generateAI: '✨ Generate with AI',
        generatingAI: 'Generating...',
        seller: 'Seller',
        provider: 'Provider',
        productName: 'Product Name',
        serviceName: 'Service Name',
        price: 'Price (COP)',
        category: 'Category',
        description: 'Description',
        iAmInterested: 'I am interested:',
        privateMsg: 'Your Private Message:',
    },
};

function App() {
    // i18n
    const [lang, setLang] = useState('es');
    const t = (key) => TRANSLATIONS[lang]?.[key] || TRANSLATIONS.es[key] || key;

    // Data State
    const [productos, setProductos] = useState([]);
    const [servicios, setServicios] = useState([]);
    const [categorias, setCategorias] = useState([]);
    const [loading, setLoading] = useState(true);

    // Filter State
    const [activeFilter, setActiveFilter] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');

    // Modal State
    const [activeModal, setActiveModal] = useState(null);
    const [consultationTarget, setConsultationTarget] = useState(null);
    const [formData, setFormData] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [apiError, setApiError] = useState(null);


    // Allied service
    const [alliedData, setAlliedData] = useState(null);

    // Toast State
    const [toasts, setToasts] = useState([]);

    useEffect(() => {
        loadData();
        loadAlliedData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const [p, s, cats] = await Promise.all([fetchProducts(), fetchServices(), fetchCategories()]);
            setProductos(p);
            setServicios(s);
            setCategorias(cats);
        } catch {
            showToast(t('loadingError'), 'error');
        } finally {
            setLoading(false);
        }
    };

    const loadAlliedData = async () => {
        try {
            const data = await fetchAlliedData();
            setAlliedData(data);
        } catch {
            setAlliedData({ disponible: false, datos: [] });
        }
    };

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

    const showToast = (message, type = 'success') => {
        const id = Date.now();
        setToasts(prev => [...prev, { id, message, type }]);
        setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
    };

    const handleInputChange = (e) => {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const openModal = (type, target = null) => {
        if (type === 'product') {
            setFormData({ vendedor_id: 'user-001', categoria_id: '' });
        } else if (type === 'service') {
            setFormData({ proveedor_id: 'user-001', categoria_id: '' });
        } else if (type === 'consultation') {
            setFormData({ comprador_id: 'user-001' });
        } else {
            setFormData({});
        }
        setApiError(null);
        setConsultationTarget(target);
        setActiveModal(type);
    };

    const closeModal = () => {
        if (!isSubmitting) {
            setActiveModal(null);
            setApiError(null);
        }
    };

    const handleSubmitProduct = async (data) => {
        setIsSubmitting(true);
        setApiError(null);
        try {
            await publishProduct(data);
            showToast(`✅ ${t('productPublished')}`);
            closeModal();
            loadData();
        } catch (err) {
            setApiError(err?.data || t('errorProduct'));
            showToast(`❌ ${t('errorProduct')}`, 'error');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleSubmitService = async (data) => {
        setIsSubmitting(true);
        setApiError(null);
        try {
            await publishService(data);
            showToast(`✅ ${t('servicePublished')}`);
            closeModal();
            loadData();
        } catch (err) {
            setApiError(err?.data || t('errorService'));
            showToast(`❌ ${t('errorService')}`, 'error');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleSubmitConsultation = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        setApiError(null);
        try {
            await sendConsultation({
                comprador_id: formData.comprador_id || 'user-003',
                item_id: consultationTarget.item.id,
                item_type: consultationTarget.type,
                mensaje: formData.mensaje || '',
            });
            showToast(`📬 ${t('messageSent')}`);
            closeModal();
        } catch (err) {
            setApiError(err?.data || t('errorMessage'));
            showToast(`❌ ${t('errorMessage')}`, 'error');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleContactClick = (item, type) => {
        openModal('consultation', { item, type });
    };

    const scrollToCatalog = () => {
        document.getElementById('catalogo')?.scrollIntoView({ behavior: 'smooth' });
    };

    const renderSkeletons = () =>
        Array.from({ length: 6 }).map((_, i) => (
            <div className="skeleton-card" key={`sk-${i}`}>
                <div className="skeleton-line w-40"></div>
                <div className="skeleton-line w-80 h-6"></div>
                <div className="skeleton-line w-full"></div>
                <div className="skeleton-line w-60"></div>
                <div className="skeleton-line w-40 h-8"></div>
                <div className="skeleton-line w-full h-10"></div>
            </div>
        ));

    return (
        <>
            <div className="background-orbs" aria-hidden="true">
                <div className="orb"></div>
                <div className="orb"></div>
                <div className="orb"></div>
            </div>

            <Navbar
                onOpenProductModal={() => openModal('product')}
                onOpenServiceModal={() => openModal('service')}
                lang={lang}
                onToggleLang={() => setLang(l => l === 'es' ? 'en' : 'es')}
            />

            <HeroSection
                productCount={productos.length}
                serviceCount={servicios.length}
                onExplore={scrollToCatalog}
                onPublish={() => openModal('product')}
            />

            <main className="container">
                <FilterBar
                    activeFilter={activeFilter}
                    onFilterChange={setActiveFilter}
                    searchQuery={searchQuery}
                    onSearchChange={setSearchQuery}
                    resultCount={filteredItems.length}
                />

                <div id="catalogo" className="grid">
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

                {/* Sección Servicio Aliado */}
                {alliedData && (
                    <section className="allied-section">
                        <h2 className="section-title">{t('alliedData')}</h2>
                        {alliedData.disponible ? (
                            <div className="allied-content">
                                <pre className="allied-json">
                                    {JSON.stringify(alliedData.datos, null, 2)}
                                </pre>
                            </div>
                        ) : (
                            <p className="allied-unavailable">{t('alliedUnavailable')}</p>
                        )}
                    </section>
                )}
            </main>

            <Footer />

            {/* Modal: Publicar Producto */}
            <ActionModal
                isOpen={activeModal === 'product'}
                onClose={closeModal}
                title={t('publishProduct')}
                subtitle={t('shareWithNeighbors')}
                isSubmitting={isSubmitting}
                submitLabel={t('confirm')}
                apiError={apiError}
                formId="product-form"
            >
                <ProductForm
                    categorias={categorias}
                    onSubmit={handleSubmitProduct}
                    t={t}
                    showToast={showToast}
                />
            </ActionModal>

            {/* Modal: Ofrecer Servicio */}
            <ActionModal
                isOpen={activeModal === 'service'}
                onClose={closeModal}
                title={t('publishService')}
                subtitle={t('offerSkills')}
                isSubmitting={isSubmitting}
                submitLabel={t('confirm')}
                apiError={apiError}
                formId="service-form"
            >
                <ServiceForm
                    categorias={categorias}
                    onSubmit={handleSubmitService}
                    t={t}
                    showToast={showToast}
                />
            </ActionModal>

            {/* Modal: Consulta */}
            <ActionModal
                isOpen={activeModal === 'consultation'}
                onClose={closeModal}
                title={`${t('contact')} — ${consultationTarget?.item?.nombre || ''}`}
                subtitle={t('privateMessage')}
                onSubmit={handleSubmitConsultation}
                isSubmitting={isSubmitting}
                submitLabel={t('confirm')}
                apiError={apiError}
            >
                <div className="form-group">
                    <label className="form-label">{t('iAmInterested')}</label>
                    <select name="comprador_id" required value={formData.comprador_id || ''} onChange={handleInputChange} className="form-select">
                        <option value="" disabled>Seleccione su cuenta...</option>
                        <option value="user-001">Juan Pérez (Apto 101)</option>
                        <option value="user-002">María García (Apto 202)</option>
                        <option value="user-003">Carlos López (Apto 303)</option>
                    </select>
                </div>
                <div className="form-group">
                    <label className="form-label">{t('privateMsg')}</label>
                    <textarea name="mensaje" rows="4" placeholder="Escribe tu mensaje o pregunta..." required value={formData.mensaje || ''} onChange={handleInputChange} className="form-textarea" />
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
