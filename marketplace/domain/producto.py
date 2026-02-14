"""Producto - artículo físico en venta con validaciones de negocio."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List

from .usuario import Usuario
from .categoria import Categoria
from .exceptions import ValidationError


@dataclass
class Producto:
    """
    Artículo físico que se puede vender en el marketplace.
    
    Validaciones de negocio:
    - Nombre: 5-100 caracteres
    - Precio: > 0, tipo Decimal para precisión monetaria
    - Stock: >= 0
    - Descripción: 10-500 caracteres (opcional)
    - Imágenes: máximo 10 URLs
    """

    id: str
    nombre: str
    precio: Decimal
    vendedor: Usuario
    descripcion: Optional[str] = None
    stock: int = 1
    categoria: Optional[Categoria] = None
    imagenes: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validar invariantes de negocio."""
        # Validar ID
        if not self.id or not self.id.strip():
            raise ValidationError("El ID del producto no puede estar vacío.")

        # Validar nombre
        if not self.nombre or not self.nombre.strip():
            raise ValidationError("El nombre del producto no puede estar vacío.")
        
        nombre_limpio = self.nombre.strip()
        if len(nombre_limpio) < 5:
            raise ValidationError("El nombre del producto debe tener al menos 5 caracteres.")
        if len(nombre_limpio) > 100:
            raise ValidationError("El nombre del producto no puede exceder 100 caracteres.")
        
        self.nombre = nombre_limpio

        # Validar precio (convertir a Decimal si es necesario)
        if isinstance(self.precio, (int, float)):
            self.precio = Decimal(str(self.precio))
        
        if not isinstance(self.precio, Decimal):
            raise ValidationError("El precio debe ser un número Decimal.")
        
        if self.precio <= 0:
            raise ValidationError(f"El precio debe ser mayor a 0. Recibido: {self.precio}")

        # Validar stock
        if not isinstance(self.stock, int):
            raise ValidationError("El stock debe ser un número entero.")
        
        if self.stock < 0:
            raise ValidationError(f"El stock no puede ser negativo. Recibido: {self.stock}")

        # Validar descripción (opcional)
        if self.descripcion is not None:
            desc_limpia = self.descripcion.strip()
            if len(desc_limpia) < 10:
                raise ValidationError("La descripción debe tener al menos 10 caracteres.")
            if len(desc_limpia) > 500:
                raise ValidationError("La descripción no puede exceder 500 caracteres.")
            
            self.descripcion = desc_limpia

        # Validar imágenes
        if len(self.imagenes) > 10:
            raise ValidationError(f"Máximo 10 imágenes permitidas. Recibido: {len(self.imagenes)}")

    def __str__(self) -> str:
        return f"{self.nombre} - ${self.precio:,.2f}"

    def hay_stock(self) -> bool:
        """Verifica si hay disponibilidad."""
        return self.stock > 0

    def reducir_stock(self, cantidad: int) -> None:
        """
        Reduce el stock del producto.
        
        Raises:
            ValidationError: Si no hay suficiente stock.
        """
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")
        
        if self.stock < cantidad:
            raise ValidationError(
                f"Stock insuficiente. Disponible: {self.stock}, Solicitado: {cantidad}"
            )
        
        self.stock -= cantidad
