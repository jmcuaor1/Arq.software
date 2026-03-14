import React from 'react';

const ItemCard = ({ item, isService, onContactClick }) => {
    const formattedPrice = new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        maximumFractionDigits: 0
    }).format(item.precio);

    const userName = isService ? item.proveedor : item.vendedor;

    return (
        <div className="glass-panel card flex flex-col justify-between">
            <div>
                <div className="meta">
                    <span style={{color: 'white', background: isService ? '#48bb78' : '#4299e1', padding: '0.2rem 0.6rem', borderRadius: '4px', fontWeight: 'bold'}}>
                        {isService ? 'Servicio' : 'Producto'}
                    </span>
                    <span>👤 {userName}</span>
                </div>
                <h3>{item.nombre}</h3>
                <div className="price">{formattedPrice}</div>
                <p className="desc">{item.descripcion || "Sin descripción adicional"}</p>
            </div>
            <button 
                className={`btn ${isService ? 'btn-secondary' : 'btn-primary'} w-100 mt-4`} 
                onClick={() => onContactClick(item, isService ? 'servicio' : 'producto')}
            >
                {isService ? 'Contactar Proveedor' : 'Contactar Vendedor'}
            </button>
        </div>
    );
};

export default ItemCard;
