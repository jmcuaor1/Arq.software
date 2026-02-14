"""Unidad Residencial con validaciones de negocio."""

from dataclasses import dataclass, field
from typing import Optional, List

from .usuario import Usuario
from .exceptions import ValidationError


@dataclass
class UnidadResidencial:
    """
    Conjunto residencial o edificio que agrupa residentes.
    
    Validaciones de negocio:
    - Nombre: 3-100 caracteres, no vacío
    - Dirección: 10-200 caracteres, no vacía
    """

    id: str
    nombre: str
    direccion: str
    residentes: List[Usuario] = field(default_factory=list)
    marketplace: Optional["Marketplace"] = None

    def __post_init__(self):
        """Validar invariantes de negocio."""
        # Validar ID
        if not self.id or not self.id.strip():
            raise ValidationError("El ID de la unidad residencial no puede estar vacío.")

        # Validar nombre
        if not self.nombre or not self.nombre.strip():
            raise ValidationError("El nombre de la unidad residencial no puede estar vacío.")
        
        nombre_limpio = self.nombre.strip()
        if len(nombre_limpio) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")
        if len(nombre_limpio) > 100:
            raise ValidationError("El nombre no puede exceder 100 caracteres.")
        
        self.nombre = nombre_limpio

        # Validar dirección
        if not self.direccion or not self.direccion.strip():
            raise ValidationError("La dirección no puede estar vacía.")
        
        dir_limpia = self.direccion.strip()
        if len(dir_limpia) < 10:
            raise ValidationError("La dirección debe tener al menos 10 caracteres.")
        if len(dir_limpia) > 200:
            raise ValidationError("La dirección no puede exceder 200 caracteres.")
        
        self.direccion = dir_limpia

    def crear_marketplace(self, nombre: str) -> "Marketplace":
        """Crea el marketplace asociado a esta unidad."""
        from .marketplace import Marketplace
        mp = Marketplace(id=f"mp-{self.id}", nombre=nombre, unidad_residencial=self)
        self.marketplace = mp
        return mp

    def registrar_residente(self, usuario: Usuario) -> None:
        """
        Registra un nuevo residente en la unidad.
        
        Raises:
            ValidationError: Si el usuario ya está registrado.
        """
        if usuario in self.residentes:
            raise ValidationError(f"El usuario {usuario.nombre} ya está registrado en esta unidad.")
        
        self.residentes.append(usuario)

    def __str__(self) -> str:
        return f"{self.nombre} - {len(self.residentes)} residentes"
