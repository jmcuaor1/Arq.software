"""Transacción - compra formalizada."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Union

from marketplace.usuario import Usuario
from marketplace.producto import Producto
from marketplace.servicio import Servicio


class EstadoTransaccion(Enum):
    """Estados posibles de una transacción."""

    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    ENTREGADA = "entregada"
    CANCELADA = "cancelada"


@dataclass
class ItemTransaccion:
    """Item comprado en una transacción."""

    item: Union[Producto, Servicio]
    cantidad: int
    precio_unitario: float

    @property
    def subtotal(self) -> float:
        return self.precio_unitario * self.cantidad


@dataclass
class Transaccion:
    """Compra formalizada entre comprador y vendedor(es)."""

    id: str
    comprador: Usuario
    items: List[ItemTransaccion] = field(default_factory=list)
    estado: EstadoTransaccion = EstadoTransaccion.PENDIENTE
    fecha: datetime = field(default_factory=datetime.now)

    @property
    def total(self) -> float:
        return sum(it.subtotal for it in self.items)

    def confirmar(self) -> None:
        """Confirma la transacción."""
        self.estado = EstadoTransaccion.CONFIRMADA

    def marcar_entregada(self) -> None:
        """Marca la transacción como entregada."""
        self.estado = EstadoTransaccion.ENTREGADA

    def cancelar(self) -> None:
        """Cancela la transacción."""
        self.estado = EstadoTransaccion.CANCELADA

    def __str__(self) -> str:
        return f"Transacción #{self.id} - {self.comprador.nombre} - ${self.total:,.0f} [{self.estado.value}]"
