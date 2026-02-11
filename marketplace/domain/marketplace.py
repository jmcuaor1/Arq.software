"""Marketplace - espacio de intercambio en una unidad residencial."""

from dataclasses import dataclass, field
from typing import List, Optional

from marketplace.unidad_residencial import UnidadResidencial
from marketplace.usuario import Usuario
from marketplace.producto import Producto
from marketplace.servicio import Servicio
from marketplace.categoria import Categoria
from marketplace.carrito import Carrito
from marketplace.transaccion import Transaccion


@dataclass
class Marketplace:
    """Espacio de intercambio donde se publican productos y servicios."""

    id: str
    nombre: str
    unidad_residencial: UnidadResidencial
    productos: List[Producto] = field(default_factory=list)
    servicios: List[Servicio] = field(default_factory=list)
    categorias: List[Categoria] = field(default_factory=list)
    transacciones: List[Transaccion] = field(default_factory=list)
    carritos: dict = field(default_factory=dict)  # usuario_id -> Carrito

    def registrar_categoria(self, categoria: Categoria) -> None:
        """Registra una categoría en el marketplace."""
        if categoria not in self.categorias:
            self.categorias.append(categoria)

    def publicar_producto(self, producto: Producto) -> None:
        """Publica un producto en el marketplace."""
        self.productos.append(producto)

    def publicar_servicio(self, servicio: Servicio) -> None:
        """Publica un servicio en el marketplace."""
        self.servicios.append(servicio)

    def buscar_productos(
        self, categoria: Optional[Categoria] = None, texto: Optional[str] = None
    ) -> List[Producto]:
        """Busca productos por categoría o texto."""
        resultados = self.productos.copy()
        if categoria:
            resultados = [p for p in resultados if p.categoria == categoria]
        if texto:
            texto_lower = texto.lower()
            resultados = [
                p
                for p in resultados
                if texto_lower in (p.nombre or "").lower()
                or texto_lower in (p.descripcion or "").lower()
            ]
        return resultados

    def buscar_servicios(
        self, categoria: Optional[Categoria] = None, solo_disponibles: bool = True
    ) -> List[Servicio]:
        """Busca servicios por categoría y disponibilidad."""
        resultados = self.servicios.copy()
        if categoria:
            resultados = [s for s in resultados if s.categoria == categoria]
        if solo_disponibles:
            resultados = [s for s in resultados if s.disponible]
        return resultados

    def obtener_carrito(self, usuario: Usuario) -> Carrito:
        """Obtiene o crea el carrito de un usuario."""
        if usuario.id not in self.carritos:
            self.carritos[usuario.id] = Carrito(usuario=usuario)
        return self.carritos[usuario.id]

    def registrar_transaccion(self, transaccion: Transaccion) -> None:
        """Registra una transacción completada."""
        self.transacciones.append(transaccion)

    def __str__(self) -> str:
        return f"Marketplace '{self.nombre}' - {len(self.productos)} productos, {len(self.servicios)} servicios"
