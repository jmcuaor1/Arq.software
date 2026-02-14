"""Transacción - compra formalizada con validaciones de negocio."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Union

from .usuario import Usuario
from .producto import Producto
from .servicio import Servicio
from .exceptions import ValidationError


class EstadoTransaccion(Enum):
    """Estados posibles de una transacción."""

    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    ENTREGADA = "entregada"
    CANCELADA = "cancelada"


@dataclass
class ItemTransaccion:
    """
    Item comprado en una transacción.
    
    Validaciones:
    - Cantidad: > 0
    - Precio unitario: > 0
    """

    item: Union[Producto, Servicio]
    cantidad: int
    precio_unitario: Decimal

    def __post_init__(self):
        """Validar invariantes de negocio."""
        # Validar cantidad
        if not isinstance(self.cantidad, int):
            raise ValidationError("La cantidad debe ser un número entero.")
        
        if self.cantidad <= 0:
            raise ValidationError(f"La cantidad debe ser mayor a 0. Recibido: {self.cantidad}")

        # Validar precio unitario (convertir a Decimal si es necesario)
        if isinstance(self.precio_unitario, (int, float)):
            self.precio_unitario = Decimal(str(self.precio_unitario))
        
        if not isinstance(self.precio_unitario, Decimal):
            raise ValidationError("El precio unitario debe ser un número Decimal.")
        
        if self.precio_unitario <= 0:
            raise ValidationError(f"El precio unitario debe ser mayor a 0. Recibido: {self.precio_unitario}")

    @property
    def subtotal(self) -> Decimal:
        """Calcula el subtotal del item."""
        return self.precio_unitario * self.cantidad


@dataclass
class Transaccion:
    """
    Compra formalizada entre comprador y vendedor(es).
    
    Validaciones:
    - Items: no vacío
    - Total: > 0 (calculado)
    """

    id: str
    comprador: Usuario
    items: List[ItemTransaccion] = field(default_factory=list)
    estado: EstadoTransaccion = EstadoTransaccion.PENDIENTE
    fecha: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validar invariantes de negocio."""
        # Validar ID
        if not self.id or not self.id.strip():
            raise ValidationError("El ID de la transacción no puede estar vacío.")

        # Validar items
        if not self.items:
            raise ValidationError("La transacción debe tener al menos un item.")

        # Validar que el total sea > 0
        if self.total <= 0:
            raise ValidationError(f"El total de la transacción debe ser mayor a 0. Total: {self.total}")

    @property
    def total(self) -> Decimal:
        """Calcula el total de la transacción."""
        return sum(it.subtotal for it in self.items)

    def confirmar(self) -> None:
        """
        Confirma la transacción.
        
        Raises:
            ValidationError: Si la transacción ya está confirmada o cancelada.
        """
        if self.estado != EstadoTransaccion.PENDIENTE:
            raise ValidationError(
                f"Solo se pueden confirmar transacciones pendientes. Estado actual: {self.estado.value}"
            )
        
        self.estado = EstadoTransaccion.CONFIRMADA

    def marcar_entregada(self) -> None:
        """
        Marca la transacción como entregada.
        
        Raises:
            ValidationError: Si la transacción no está confirmada.
        """
        if self.estado != EstadoTransaccion.CONFIRMADA:
            raise ValidationError(
                f"Solo se pueden entregar transacciones confirmadas. Estado actual: {self.estado.value}"
            )
        
        self.estado = EstadoTransaccion.ENTREGADA

    def cancelar(self) -> None:
        """
        Cancela la transacción.
        
        Raises:
            ValidationError: Si la transacción ya está entregada.
        """
        if self.estado == EstadoTransaccion.ENTREGADA:
            raise ValidationError("No se pueden cancelar transacciones entregadas.")
        
        self.estado = EstadoTransaccion.CANCELADA

    def __str__(self) -> str:
        return f"Transacción #{self.id} - {self.comprador.nombre} - ${self.total:,.2f} [{self.estado.value}]"
