"""Carrito de compras."""

from dataclasses import dataclass, field
from typing import List, Union

from marketplace.usuario import Usuario
from marketplace.producto import Producto
from marketplace.servicio import Servicio


@dataclass
class ItemCarrito:
    """Item en el carrito: puede ser producto o servicio."""

    item: Union[Producto, Servicio]
    cantidad: int = 1

    @property
    def subtotal(self) -> float:
        return self.item.precio * self.cantidad

    def __str__(self) -> str:
        return f"{self.item.nombre} x{self.cantidad} = ${self.subtotal:,.0f}"


@dataclass
class Carrito:
    """Carrito de compras de un usuario."""

    usuario: Usuario
    items: List[ItemCarrito] = field(default_factory=list)

    def agregar(self, item: Union[Producto, Servicio], cantidad: int = 1) -> None:
        """Agrega un producto o servicio al carrito."""
        for ic in self.items:
            if ic.item.id == item.id and type(ic.item) == type(item):
                ic.cantidad += cantidad
                return
        self.items.append(ItemCarrito(item=item, cantidad=cantidad))

    def quitar(self, item: Union[Producto, Servicio]) -> bool:
        """Elimina un item del carrito. Retorna True si se eliminó."""
        for i, ic in enumerate(self.items):
            if ic.item.id == item.id and type(ic.item) == type(item):
                self.items.pop(i)
                return True
        return False

    @property
    def total(self) -> float:
        return sum(ic.subtotal for ic in self.items)

    def vaciar(self) -> None:
        """Vacía el carrito."""
        self.items.clear()

    def __str__(self) -> str:
        if not self.items:
            return f"Carrito de {self.usuario.nombre}: vacío"
        return f"Carrito de {self.usuario.nombre}: {len(self.items)} items - Total: ${self.total:,.0f}"
