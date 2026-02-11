"""Usuario/Residente del marketplace."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Usuario:
    """Residente que puede vender productos, ofrecer servicios y comprar."""

    id: str
    nombre: str
    email: str
    apartamento: Optional[str] = None  # Ej: "101", "A-202"
    telefono: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.nombre} ({self.apartamento or 'Sin apto'})"
