"""Servicio ofrecido por residentes."""

from dataclasses import dataclass
from typing import Optional

from marketplace.usuario import Usuario
from marketplace.categoria import Categoria


@dataclass
class Servicio:
    """Servicio que un residente ofrece a otros en el marketplace."""

    id: str
    nombre: str
    precio: float
    proveedor: Usuario
    descripcion: Optional[str] = None
    disponible: bool = True
    categoria: Optional[Categoria] = None

    def __str__(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"{self.nombre} - ${self.precio:,.0f} [{estado}]"
