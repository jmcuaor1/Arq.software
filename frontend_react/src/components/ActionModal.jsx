import React, { useEffect, useRef } from 'react';

const ActionModal = ({ isOpen, onClose, title, subtitle, onSubmit, children }) => {
    const dialogRef = useRef(null);

    useEffect(() => {
        if (!isOpen) return;

        const handleKeyDown = (e) => {
            if (e.key === 'Escape') onClose();
        };

        document.addEventListener('keydown', handleKeyDown);
        document.body.style.overflow = 'hidden';

        // Focus trap: focus first input
        const timer = setTimeout(() => {
            const firstInput = dialogRef.current?.querySelector('input, select, textarea');
            firstInput?.focus();
        }, 100);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
            document.body.style.overflow = '';
            clearTimeout(timer);
        };
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    const handleOverlayClick = (e) => {
        if (e.target === e.currentTarget) onClose();
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
                >
                    ✕
                </button>

                <div className="modal-header">
                    <h2 className="modal-title" id="modal-title">{title}</h2>
                    {subtitle && <p className="modal-subtitle">{subtitle}</p>}
                </div>

                <form onSubmit={onSubmit}>
                    {children}
                    <div className="form-submit">
                        <button type="submit" className="btn btn-primary btn-full btn-lg">
                            Confirmar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ActionModal;
