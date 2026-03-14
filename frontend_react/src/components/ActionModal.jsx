import React, { useState } from 'react';

const ActionModal = ({ isOpen, onClose, title, onSubmit, children }) => {
    if (!isOpen) return null;

    return (
        <div className="modal show">
            <div className="modal-content glass-panel" style={{position: 'relative'}}>
                <span className="close-btn" onClick={onClose}>&times;</span>
                <h2 style={{ marginBottom: '1rem', background: 'linear-gradient(to right, #4299e1, #48bb78)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                    {title}
                </h2>
                <form onSubmit={onSubmit}>
                    {children}
                </form>
            </div>
        </div>
    );
};

export default ActionModal;
