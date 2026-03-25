import React from 'react';

const Navbar = ({ onOpenProductModal, onOpenServiceModal }) => {
    return (
        <header className="navbar">
            <div className="container navbar-inner">
                <a className="navbar-brand" href="/" aria-label="VecinoMarket inicio">
                    <div className="navbar-logo" aria-hidden="true">V</div>
                    <span className="navbar-brand-text">VecinoMarket</span>
                </a>

                <nav className="navbar-actions" aria-label="Acciones principales">
                    <button
                        className="btn btn-secondary"
                        onClick={onOpenServiceModal}
                        id="btn-offer-service"
                    >
                        <span className="btn-icon" aria-hidden="true">⚡</span>
                        Ofrecer Servicio
                    </button>
                    <button
                        className="btn btn-primary"
                        onClick={onOpenProductModal}
                        id="btn-publish-product"
                    >
                        <span className="btn-icon" aria-hidden="true">+</span>
                        Publicar Producto
                    </button>
                </nav>
            </div>
        </header>
    );
};

export default Navbar;
