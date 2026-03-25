import React from 'react';

const HeroSection = ({ productCount, serviceCount, onExplore, onPublish }) => {
    return (
        <section className="hero">
            <div className="container">
                <div className="hero-badge">
                    <span className="hero-badge-dot"></span>
                    Marketplace activo — Sprint 1
                </div>

                <h1>
                    Tu comunidad,{' '}
                    <span className="gradient-text">tu marketplace</span>
                </h1>

                <p className="hero-subtitle">
                    Conecta con tus vecinos, publica productos y ofrece servicios
                    dentro de tu unidad residencial. Todo en un solo lugar.
                </p>

                <div className="hero-actions">
                    <button className="btn btn-accent btn-lg" onClick={onExplore}>
                        Explorar catálogo ↓
                    </button>
                    <button className="btn btn-secondary btn-lg" onClick={onPublish}>
                        + Publicar algo
                    </button>
                </div>

                <div className="hero-stats">
                    <div className="hero-stat">
                        <div className="hero-stat-value">{productCount}</div>
                        <div className="hero-stat-label">Productos</div>
                    </div>
                    <div className="hero-stat-divider" aria-hidden="true"></div>
                    <div className="hero-stat">
                        <div className="hero-stat-value">{serviceCount}</div>
                        <div className="hero-stat-label">Servicios</div>
                    </div>
                    <div className="hero-stat-divider" aria-hidden="true"></div>
                    <div className="hero-stat">
                        <div className="hero-stat-value">{productCount + serviceCount}</div>
                        <div className="hero-stat-label">Publicaciones</div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default HeroSection;
