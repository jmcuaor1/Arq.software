import React, { useEffect, useRef } from 'react';

const ActionModal = ({
    isOpen,
    onClose,
    title,
    subtitle,
    onSubmit,
    children,
    isSubmitting = false,
    submitLabel = 'Confirmar',
    apiError = null,
}) => {
    const dialogRef = useRef(null);

    useEffect(() => {
        if (!isOpen) return;

        const handleKeyDown = (e) => {
            if (e.key === 'Escape' && !isSubmitting) onClose();
        };

        document.addEventListener('keydown', handleKeyDown);
        document.body.style.overflow = 'hidden';

        const timer = setTimeout(() => {
            const firstInput = dialogRef.current?.querySelector('input, select, textarea');
            firstInput?.focus();
        }, 100);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
            document.body.style.overflow = '';
            clearTimeout(timer);
        };
    }, [isOpen, onClose, isSubmitting]);

    if (!isOpen) return null;

    const handleOverlayClick = (e) => {
        if (e.target === e.currentTarget && !isSubmitting) onClose();
    };

    return (
        <div
            className="modal-overlay"
            onClick={handleOverlayClick}
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
        >
            <div className="modal-content" ref={dialogRef}>
                <button
                    className="modal-close"
                    onClick={onClose}
                    aria-label="Cerrar diálogo"
                    type="button"
                    disabled={isSubmitting}
                >
                    ✕
                </button>

                <div className="modal-header">
                    <h2 className="modal-title" id="modal-title">{title}</h2>
                    {subtitle && <p className="modal-subtitle">{subtitle}</p>}
                </div>

                <form onSubmit={onSubmit} noValidate>
                    {children}

                    {apiError && (
                        <div className="form-api-error" role="alert">
                            {typeof apiError === 'string'
                                ? apiError
                                : Object.entries(apiError).map(([k, v]) => (
                                    <div key={k}><strong>{k}:</strong> {Array.isArray(v) ? v.join(', ') : v}</div>
                                ))
                            }
                        </div>
                    )}

                    <div className="form-submit">
                        <button
                            type="submit"
                            className="btn btn-primary btn-full btn-lg"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? (
                                <span className="btn-loading">
                                    <span className="spinner" aria-hidden="true"></span>
                                    Procesando...
                                </span>
                            ) : submitLabel}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ActionModal;
