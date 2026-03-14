const API_URL = 'http://127.0.0.1:8000/api';

export const fetchProducts = async () => {
    const response = await fetch(`${API_URL}/productos/`);
    if (!response.ok) throw new Error('Error fetching products');
    return response.json();
};

export const fetchServices = async () => {
    const response = await fetch(`${API_URL}/servicios/`);
    if (!response.ok) throw new Error('Error fetching services');
    return response.json();
};

export const publishProduct = async (productData) => {
    const response = await fetch(`${API_URL}/productos/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(productData),
    });
    if (!response.ok) {
        const errData = await response.json();
        throw new Error(JSON.stringify(errData));
    }
    return response.json();
};

export const publishService = async (serviceData) => {
    const response = await fetch(`${API_URL}/servicios/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(serviceData),
    });
    if (!response.ok) {
        const errData = await response.json();
        throw new Error(JSON.stringify(errData));
    }
    return response.json();
};

export const sendConsultation = async (consultationData) => {
    const response = await fetch(`${API_URL}/consultas/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(consultationData),
    });
    if (!response.ok) {
        const errData = await response.json();
        throw new Error(JSON.stringify(errData));
    }
    return response.json();
};
