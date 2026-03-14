import React from 'react';

const Navbar = ({ onOpenProductModal, onOpenServiceModal }) => {
    return (
        <header className="glass-header">
            <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1>VecinoMarket</h1>
                    <p>Conectando el ecosistema de la Unidad Residencial</p>
                </div>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <button className="btn btn-primary" onClick={onOpenProductModal}>
                        + Publicar Producto
                    </button>
                    <button className="btn btn-secondary" onClick={onOpenServiceModal}>
                        + Ofrecer Servicio
                    </button>
                </div>
            </div>
        </header>
    );
};

export default Navbar;
