const API_URL = 'http://44.207.202.98:8080/api';

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

export const fetchUsers = async () => {
    const response = await fetch(`${API_URL}/usuarios/`);
    if (!response.ok) throw new Error('Error fetching users');
    return response.json();
};

export const fetchCategories = async () => {
    const response = await fetch(`${API_URL}/categorias/`);
    if (!response.ok) throw new Error('Error fetching categories');
    return response.json();
};

export const publishProduct = async (productData) => {
    const response = await fetch(`${API_URL}/productos/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(productData),
    });
    const data = await response.json();
    if (!response.ok) throw { status: response.status, data };
    return data;
};

export const publishService = async (serviceData) => {
    const response = await fetch(`${API_URL}/servicios/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(serviceData),
    });
    const data = await response.json();
    if (!response.ok) throw { status: response.status, data };
    return data;
};

export const sendConsultation = async (consultationData) => {
    const response = await fetch(`${API_URL}/consultas/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(consultationData),
    });
    const data = await response.json();
    if (!response.ok) throw { status: response.status, data };
    return data;
};

export const generarDescripcion = async (nombre) => {
    const response = await fetch(`${API_URL}/ai/generar-descripcion/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre }),
    });
    if (!response.ok) return { descripcion: '' };
    return response.json();
};

export const fetchAlliedData = async () => {
    const response = await fetch(`${API_URL}/aliado/datos-externos/`);
    if (!response.ok) return { disponible: false, datos: [] };
    return response.json();
};

export const fetchCatalogPublico = async () => {
    const response = await fetch(`${API_URL}/aliado/catalogo/`);
    if (!response.ok) throw new Error('Error fetching public catalog');
    return response.json();
};
