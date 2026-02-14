"""Servicio ofrecido por residentes con validaciones de negocio."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from .usuario import Usuario
from .categoria import Categoria
from .exceptions import ValidationError


@dataclass
class Servicio:
    """
    Servicio que un residente ofrece a otros en el marketplace.
    
    Validaciones de negocio:
    - Nombre: 5-100 caracteres
    - Precio: > 0, tipo Decimal para precisión monetaria
    - Descripción: 10-500 caracteres (opcional)
    """

    id: str
    nombre: str
    precio: Decimal
    proveedor: Usuario
    descripcion: Optional[str] = None
    disponible: bool = True
    categoria: Optional[Categoria] = None

    def __post_init__(self):
        """Validar invariantes de negocio."""
        # Validar ID
        if not self.id or not self.id.strip():
            raise ValidationError("El ID del servicio no puede estar vacío.")

        # Validar nombre
        if not self.nombre or not self.nombre.strip():
            raise ValidationError("El nombre del servicio no puede estar vacío.")
        
        nombre_limpio = self.nombre.strip()
        if len(nombre_limpio) < 5:
            raise ValidationError("El nombre del servicio debe tener al menos 5 caracteres.")
        if len(nombre_limpio) > 100:
            raise ValidationError("El nombre del servicio no puede exceder 100 caracteres.")
        
        self.nombre = nombre_limpio

        # Validar precio (convertir a Decimal si es necesario)
        if isinstance(self.precio, (int, float)):
            self.precio = Decimal(str(self.precio))
        
        if not isinstance(self.precio, Decimal):
            raise ValidationError("El precio debe ser un número Decimal.")
        
        if self.precio <= 0:
            raise ValidationError(f"El precio debe ser mayor a 0. Recibido: {self.precio}")

        # Validar descripción (opcional)
        if self.descripcion is not None:
            desc_limpia = self.descripcion.strip()
            if len(desc_limpia) < 10:
                raise ValidationError("La descripción debe tener al menos 10 caracteres.")
            if len(desc_limpia) > 500:
                raise ValidationError("La descripción no puede exceder 500 caracteres.")
            
            self.descripcion = desc_limpia

    def __str__(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"{self.nombre} - ${self.precio:,.2f} [{estado}]"

    def marcar_no_disponible(self) -> None:
        """Marca el servicio como no disponible."""
        self.disponible = False

    def marcar_disponible(self) -> None:
        """Marca el servicio como disponible."""
        self.disponible = True
