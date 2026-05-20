import { useState } from 'react';

export default function ServiceForm({ categorias, onSubmit, t }) {
    const [formData, setFormData] = useState({ proveedor_id: 'user-001', categoria_id: '', nombre: '', precio: '', descripcion: '' });

    const handleChange = (e) => {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({
            ...formData,
            precio: Math.round(parseFloat(formData.precio)),
            proveedor_status: 'APPROVED',
        });
    };

    return (
        <form onSubmit={handleSubmit} id="service-form">
            <div className="form-group">
                <label className="form-label">{t('provider')}</label>
                <select name="proveedor_id" required value={formData.proveedor_id} onChange={handleChange} className="form-select">
                    <option value="user-001">Juan Pérez (Apto 101)</option>
                    <option value="user-002">María García (Apto 202)</option>
                </select>
            </div>
            <div className="form-group">
                <label className="form-label">{t('serviceName')}</label>
                <input type="text" name="nombre" placeholder="Ej: Paseo de Perros..." required value={formData.nombre} onChange={handleChange} className="form-input" />
            </div>
            <div className="form-group">
                <label className="form-label">{t('price')}</label>
                <input type="number" name="precio" placeholder="25000" min="1" required value={formData.precio} onChange={handleChange} className="form-input" />
            </div>
            <div className="form-group">
                <label className="form-label">{t('category')}</label>
                <select name="categoria_id" required value={formData.categoria_id} onChange={handleChange} className="form-select">
                    <option value="" disabled>Seleccione categoría...</option>
                    {categorias.map(c => (
                        <option key={c.id} value={c.id}>{c.nombre}</option>
                    ))}
                </select>
            </div>
            <div className="form-group">
                <label className="form-label">{t('description')}</label>
                <textarea name="descripcion" rows="3" placeholder="Disponibilidad, herramientas..." value={formData.descripcion} onChange={handleChange} className="form-textarea" />
            </div>
        </form>
    );
}
