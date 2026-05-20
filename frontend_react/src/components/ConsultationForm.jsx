import { useState } from 'react';

export default function ConsultationForm({ onSubmit, t }) {
    const [formData, setFormData] = useState({ comprador_id: 'user-001', mensaje: '' });

    const handleChange = (e) => {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit} id="consultation-form">
            <div className="form-group">
                <label className="form-label">{t('iAmInterested')}</label>
                <select name="comprador_id" required value={formData.comprador_id} onChange={handleChange} className="form-select">
                    <option value="user-001">Juan Pérez (Apto 101)</option>
                    <option value="user-002">María García (Apto 202)</option>
                    <option value="user-003">Carlos López (Apto 303)</option>
                </select>
            </div>
            <div className="form-group">
                <label className="form-label">{t('privateMsg')}</label>
                <textarea name="mensaje" rows="4" placeholder={t('placeholderMessage')} required value={formData.mensaje} onChange={handleChange} className="form-textarea" />
            </div>
        </form>
    );
}
