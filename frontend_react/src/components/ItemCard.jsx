import React from 'react';

const ItemCard = ({ item, isService, onContactClick }) => {
    const formattedPrice = new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        maximumFractionDigits: 0,
    }).format(item.precio);

    const userName = isService ? item.proveedor : item.vendedor;
    const initials = userName
        ? userName.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
        : '??';

    return (
        <article className="card" id={`card-${isService ? 's' : 'p'}-${item.id}`}>
            <div className="card-header">
                <span className={`card-badge ${isService ? 'card-badge-service' : 'card-badge-product'}`}>
                    {isService ? '⚡ Servicio' : '📦 Producto'}
                </span>
                <div className="card-seller">
                    <div className="card-seller-avatar" aria-hidden="true">{initials}</div>
                    <span>{userName}</span>
                </div>
            </div>

            <h3 className="card-title">{item.nombre}</h3>
            <p className="card-description">{item.descripcion || 'Sin descripción adicional'}</p>
            <div className="card-price">{formattedPrice}</div>

            <button
                className={`btn ${isService ? 'btn-secondary' : 'btn-primary'} btn-full card-action`}
                onClick={() => onContactClick(item, isService ? 'servicio' : 'producto')}
                id={`contact-${isService ? 's' : 'p'}-${item.id}`}
            >
                {isService ? '💬 Contactar Proveedor' : '💬 Contactar Vendedor'}
            </button>
        </article>
    );
};

export default ItemCard;
