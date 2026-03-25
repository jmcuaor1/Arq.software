import React from 'react';

const EmptyState = ({ onPublishProduct, onPublishService }) => {
    return (
        <div className="empty-state">
            <div className="empty-state-icon">🏘️</div>
            <h3 className="empty-state-title">Aún no hay publicaciones</h3>
            <p className="empty-state-text">
                Sé el primero en publicar un producto o servicio en tu comunidad residencial.
            </p>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
                <button className="btn btn-primary" onClick={onPublishProduct}>
                    + Publicar Producto
                </button>
                <button className="btn btn-secondary" onClick={onPublishService}>
                    + Ofrecer Servicio
                </button>
            </div>
        </div>
    );
};

export default EmptyState;
