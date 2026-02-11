"""Unidad Residencial - conjunto/edificio residencial."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from marketplace.marketplace import Marketplace
from marketplace.usuario import Usuario


@dataclass
class UnidadResidencial:
    """Conjunto residencial (edificio, torre, barrio cerrado)."""

    id: str
    nombre: str
    direccion: str
    marketplace: Optional[Marketplace] = None
    residentes: List[Usuario] = field(default_factory=list)

    def crear_marketplace(self, nombre: str) -> "Marketplace":
        """Crea el marketplace asociado a esta unidad."""
        from marketplace.marketplace import Marketplace
        mp = Marketplace(id=f"mp-{self.id}", nombre=nombre, unidad_residencial=self)
        self.marketplace = mp
        return mp

    def registrar_residente(self, usuario: Usuario) -> None:
        """Registra un residente en la unidad."""
        if usuario not in self.residentes:
            self.residentes.append(usuario)

    def obtener_marketplace(self) -> Optional["Marketplace"]:
        """Obtiene el marketplace de la unidad."""
        return self.marketplace

    def __str__(self) -> str:
        return f"{self.nombre} - {self.direccion}"
