import { useState } from 'react';

export default function ProductForm({ categorias, onSubmit, t }) {
    const [formData, setFormData] = useState({ vendedor_id: 'user-001', categoria_id: '', nombre: '', precio: '', descripcion: '' });

    const handleChange = (e) => {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({
            ...formData,
            precio: Math.round(parseFloat(formData.precio)),
            vendedor_status: 'APPROVED',
        });
    };

    return (
        <form onSubmit={handleSubmit} id="product-form">
            <div className="form-group">
                <label className="form-label">{t('seller')}</label>
                <select name="vendedor_id" required value={formData.vendedor_id} onChange={handleChange} className="form-select">
                    <option value="user-001">Juan Pérez (Apto 101)</option>
                    <option value="user-002">María García (Apto 202)</option>
                </select>
            </div>
            <div className="form-group">
                <label className="form-label">{t('productName')}</label>
                <input type="text" name="nombre" placeholder={t('placeholderProductName')} required value={formData.nombre} onChange={handleChange} className="form-input" />
            </div>
            <div className="form-group">
                <label className="form-label">{t('price')}</label>
                <input type="number" name="precio" placeholder={t('placeholderPrice')} min="1" required value={formData.precio} onChange={handleChange} className="form-input" />
            </div>
            <div className="form-group">
                <label className="form-label">{t('category')}</label>
                <select name="categoria_id" required value={formData.categoria_id} onChange={handleChange} className="form-select">
                    <option value="" disabled>{t('selectCategory')}</option>
                    {categorias.map(c => (
                        <option key={c.id} value={c.id}>{c.nombre}</option>
                    ))}
                </select>
            </div>
            <div className="form-group">
                <label className="form-label">{t('description')}</label>
                <textarea name="descripcion" rows="3" placeholder={t('placeholderDescription')} value={formData.descripcion} onChange={handleChange} className="form-textarea" />
            </div>
        </form>
    );
}
