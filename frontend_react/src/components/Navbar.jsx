import React from 'react';

const Navbar = ({ onOpenProductModal, onOpenServiceModal, lang = 'es', onToggleLang, onOpenConsultas }) => {
    return (
        <header className="navbar">
            <div className="container navbar-inner">
                <a className="navbar-brand" href="/" aria-label="VecinoMarket inicio">
                    <div className="navbar-logo" aria-hidden="true">V</div>
                    <span className="navbar-brand-text">VecinoMarket</span>
                </a>

                <nav className="navbar-actions" aria-label="Acciones principales">
                    <button
                        className="btn btn-lang"
                        onClick={onToggleLang}
                        aria-label={`Cambiar idioma a ${lang === 'es' ? 'English' : 'Español'}`}
                        title={lang === 'es' ? 'Switch to English' : 'Cambiar a Español'}
                    >
                        {lang === 'es' ? '🇨🇴 ES' : '🇺🇸 EN'}
                    </button>
                    <button
                        className="btn btn-secondary"
                        onClick={onOpenConsultas}
                        id="btn-consultas"
                    >
                        <span className="btn-icon" aria-hidden="true">📬</span>
                        {lang === 'es' ? 'Mis Consultas' : 'My Consultations'}
                    </button>
                    <button
                        className="btn btn-secondary"
                        onClick={onOpenServiceModal}
                        id="btn-offer-service"
                    >
                        <span className="btn-icon" aria-hidden="true">⚡</span>
                        {lang === 'es' ? 'Ofrecer Servicio' : 'Offer Service'}
                    </button>
                    <button
                        className="btn btn-primary"
                        onClick={onOpenProductModal}
                        id="btn-publish-product"
                    >
                        <span className="btn-icon" aria-hidden="true">+</span>
                        {lang === 'es' ? 'Publicar Producto' : 'Publish Product'}
                    </button>
                </nav>
            </div>
        </header>
    );
};

export default Navbar;
