import React from 'react';

const FilterBar = ({ activeFilter, onFilterChange, searchQuery, onSearchChange, resultCount }) => {
    const filters = [
        { key: 'all', label: 'Todos' },
        { key: 'products', label: 'Productos' },
        { key: 'services', label: 'Servicios' },
    ];

    return (
        <div className="filter-bar" id="catalogo">
            <div className="filter-tabs" role="tablist" aria-label="Filtrar publicaciones">
                {filters.map(f => (
                    <button
                        key={f.key}
                        role="tab"
                        aria-selected={activeFilter === f.key}
                        className={`filter-tab${activeFilter === f.key ? ' active' : ''}`}
                        onClick={() => onFilterChange(f.key)}
                    >
                        {f.label}
                    </button>
                ))}
            </div>

            <div className="filter-search">
                <span className="filter-search-icon" aria-hidden="true">🔍</span>
                <input
                    type="text"
                    placeholder="Buscar por nombre..."
                    value={searchQuery}
                    onChange={(e) => onSearchChange(e.target.value)}
                    aria-label="Buscar publicaciones"
                />
            </div>

            <span className="filter-results">
                {resultCount} resultado{resultCount !== 1 ? 's' : ''}
            </span>
        </div>
    );
};

export default FilterBar;
