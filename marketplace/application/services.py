from dataclasses import dataclass
from typing import List

from ..domain.exceptions import PermissionError
from ..domain.usuario import Usuario
from ..domain.categoria import Categoria
from ..domain.builders import ProductoBuilder
from ..infrastructure.factories import NotifierFactory
from ..infrastructure.repositories import ProductoRepository

@dataclass(frozen=True)
class PublicarProductoCommand:
    vendedor: Usuario
    vendedor_status: str      # "APPROVED" etc.
    nombre: str
    descripcion: str
    precio_cop: int
    categoria: Categoria
    imagenes: List[str]

class PublicacionService:
    def __init__(self, repo: ProductoRepository, max_images: int = 4):
        self.repo = repo
        self.max_images = max_images

    def publicar_producto(self, cmd: PublicarProductoCommand):
        if cmd.vendedor_status != "APPROVED":
            raise PermissionError("Solo usuarios APPROVED pueden publicar.")

        builder = (
            ProductoBuilder(max_images=self.max_images)
            .vendedor(cmd.vendedor)
            .categoria(cmd.categoria)
            .nombre(cmd.nombre)
            .descripcion(cmd.descripcion)
            .precio_cop(cmd.precio_cop)
        )

        for url in cmd.imagenes[: self.max_images]:
            builder.add_imagen(url)

        producto = builder.build()
        self.repo.add(producto)

        notifier = NotifierFactory.create()
        notifier.notify_listing_created(cmd.vendedor.telefono, producto.nombre)

        return producto
