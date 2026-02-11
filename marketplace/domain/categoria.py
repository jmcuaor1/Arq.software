"""Categoría para clasificar productos y servicios."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Categoria:
    """Clasificación de productos y servicios en el marketplace."""

    id: str
    nombre: str
    descripcion: Optional[str] = None

    def __str__(self) -> str:
        return self.nombre
