"""Producto - artículo físico en venta."""

from dataclasses import dataclass
from typing import Optional

from marketplace.usuario import Usuario
from marketplace.categoria import Categoria


@dataclass
class Producto:
    """Artículo físico que se puede vender en el marketplace."""

    id: str
    nombre: str
    precio: float
    vendedor: Usuario
    descripcion: Optional[str] = None
    stock: int = 1
    categoria: Optional[Categoria] = None

    def __str__(self) -> str:
        return f"{self.nombre} - ${self.precio:,.0f}"

    def hay_stock(self) -> bool:
        """Verifica si hay disponibilidad."""
        return self.stock > 0
