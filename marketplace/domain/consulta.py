"""Consulta - registro de interés de un comprador en un producto o servicio."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Union

from .usuario import Usuario
from .producto import Producto
from .servicio import Servicio
from .exceptions import ValidationError


class EstadoConsulta(Enum):
    """Estados posibles de una consulta."""

    PENDIENTE = "pendiente"      # Consulta enviada
    CONTACTADO = "contactado"    # El vendedor ya contactó o respondió
    CERRADA = "cerrada"          # El ciclo de contacto terminó


@dataclass
class Consulta:
    """
    Registro de interés de un comprador en un producto o servicio.
    No implica transacción, solo facilita la conexión.
    """

    id: str
    comprador: Usuario
    item: Union[Producto, Servicio]
    mensaje: Optional[str] = None
    fecha: datetime = field(default_factory=datetime.now)
    estado: EstadoConsulta = EstadoConsulta.PENDIENTE

    def __post_init__(self):
        """Validar invariantes de negocio."""
        if not self.id or not self.id.strip():
            raise ValidationError("El ID de la consulta no puede estar vacío.")
        
        if not self.comprador:
            raise ValidationError("La consulta debe tener un comprador.")
            
        if not self.item:
            raise ValidationError("La consulta debe referirse a un producto o servicio.")

    def marcar_contactado(self) -> None:
        """Marca la consulta como contactada."""
        self.estado = EstadoConsulta.CONTACTADO

    def cerrar(self) -> None:
        """Cierra la consulta."""
        self.estado = EstadoConsulta.CERRADA

    def __str__(self) -> str:
        return f"Consulta #{self.id} - {self.comprador.nombre} interesada en '{self.item.nombre}' [{self.estado.value}]"
