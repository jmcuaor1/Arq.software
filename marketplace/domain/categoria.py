"""Categoría para clasificar productos y servicios con validaciones."""

from dataclasses import dataclass
from typing import Optional

from .exceptions import ValidationError


@dataclass
class Categoria:
    """
    Clasificación de productos y servicios en el marketplace.
    
    Validaciones de negocio:
    - Nombre: 3-50 caracteres, no vacío
    - Descripción: máximo 200 caracteres (opcional)
    """

    id: str
    nombre: str
    descripcion: Optional[str] = None

    def __post_init__(self):
        """Validar invariantes de negocio."""
        # Validar ID
        if not self.id or not self.id.strip():
            raise ValidationError("El ID de la categoría no puede estar vacío.")

        # Validar nombre
        if not self.nombre or not self.nombre.strip():
            raise ValidationError("El nombre de la categoría no puede estar vacío.")
        
        nombre_limpio = self.nombre.strip()
        if len(nombre_limpio) < 3:
            raise ValidationError("El nombre de la categoría debe tener al menos 3 caracteres.")
        if len(nombre_limpio) > 50:
            raise ValidationError("El nombre de la categoría no puede exceder 50 caracteres.")
        
        self.nombre = nombre_limpio

        # Validar descripción (opcional)
        if self.descripcion is not None:
            desc_limpia = self.descripcion.strip()
            if len(desc_limpia) > 200:
                raise ValidationError("La descripción no puede exceder 200 caracteres.")
            
            self.descripcion = desc_limpia if desc_limpia else None

    def __str__(self) -> str:
        return self.nombre
