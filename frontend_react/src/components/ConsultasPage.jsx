import { useState, useEffect } from 'react';
import { fetchConsultasVendedor } from '../services/api';

const USUARIOS = [
    { id: 'user-001', nombre: 'Juan Pérez (Apto 101)' },
    { id: 'user-002', nombre: 'María García (Apto 202)' },
    { id: 'user-003', nombre: 'Carlos López (Apto 303)' },
];

export default function ConsultasPage({ onBack, lang }) {
    const t = (es, en) => lang === 'es' ? es : en;
    const [vendedorId, setVendedorId] = useState('user-001');
    const [consultas, setConsultas] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        cargarConsultas(vendedorId);
    }, [vendedorId]);

    const cargarConsultas = async (id) => {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchConsultasVendedor(id);
            setConsultas(data);
        } catch {
            setError(t('Error cargando consultas', 'Error loading consultations'));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ paddingTop: '2rem', paddingBottom: '4rem' }}>
            <button className="btn btn-secondary" onClick={onBack} style={{ marginBottom: '1.5rem' }}>
                ← {t('Volver al catálogo', 'Back to catalog')}
            </button>

            <h1 style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '0.5rem' }}>
                {t('Mis Consultas Recibidas', 'My Received Consultations')}
            </h1>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
                {t('Mensajes que han enviado sobre tus publicaciones', 'Messages sent about your listings')}
            </p>

            <div className="form-group" style={{ maxWidth: '360px', marginBottom: '2rem' }}>
                <label className="form-label">{t('Ver consultas de:', 'View consultations for:')}</label>
                <select
                    value={vendedorId}
                    onChange={e => setVendedorId(e.target.value)}
                    className="form-select"
                >
                    {USUARIOS.map(u => (
                        <option key={u.id} value={u.id}>{u.nombre}</option>
                    ))}
                </select>
            </div>

            {loading && (
                <div style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '2rem' }}>
                    {t('Cargando...', 'Loading...')}
                </div>
            )}

            {error && (
                <div className="form-api-error">{error}</div>
            )}

            {!loading && !error && consultas.length === 0 && (
                <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📭</div>
                    <p>{t('No hay consultas recibidas aún', 'No consultations received yet')}</p>
                </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {consultas.map(c => (
                    <div key={c.id} className="item-card" style={{ padding: '1.5rem' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                            <div>
                                <span style={{ fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', color: 'var(--accent-primary)', letterSpacing: '0.05em' }}>
                                    {c.item_nombre}
                                </span>
                                <p style={{ fontWeight: 600, marginTop: '0.25rem' }}>
                                    {t('De:', 'From:')} {c.comprador_nombre}
                                </p>
                            </div>
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', whiteSpace: 'nowrap' }}>
                                {c.estado}
                            </span>
                        </div>
                        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.6, background: 'rgba(255,255,255,0.03)', padding: '0.75rem', borderRadius: '8px', borderLeft: '3px solid var(--accent-primary)' }}>
                            "{c.mensaje || t('Sin mensaje', 'No message')}"
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}
