"""Service Layer - Orquestación de lógica de negocio siguiendo SOLID."""

from dataclasses import dataclass
from typing import List, Optional

from ..domain.exceptions import DomainError, PermissionError, ValidationError
from ..domain.usuario import Usuario
from ..domain.unidad_residencial import UnidadResidencial
from ..domain.categoria import Categoria
from ..domain.producto import Producto
from ..domain.builders import ProductoBuilder
from ..infrastructure.factories import NotifierFactory
from ..infrastructure.repositories import (
    InMemoryUsuarioRepository,
    InMemoryUnidadResidencialRepository,
    InMemoryCategoriaRepository,
    InMemoryProductoRepository,
)


# ============================================================================
# Commands (DTOs para entrada de servicios)
# ============================================================================

@dataclass(frozen=True)
class CrearUsuarioCommand:
    """Comando para crear un usuario."""
    id: str
    nombre: str
    email: str
    apartamento: Optional[str] = None
    telefono: Optional[str] = None


@dataclass(frozen=True)
class CrearUnidadResidencialCommand:
    """Comando para crear una unidad residencial."""
    id: str
    nombre: str
    direccion: str


@dataclass(frozen=True)
class CrearCategoriaCommand:
    """Comando para crear una categoría."""
    id: str
    nombre: str
    descripcion: str


@dataclass(frozen=True)
class PublicarProductoCommand:
    """Comando para publicar un producto."""
    vendedor_id: str
    vendedor_status: str
    nombre: str
    descripcion: str
    precio_cop: int
    categoria_id: str
    imagenes: List[str]


# ============================================================================
# Excepciones de Aplicación
# ============================================================================

class ResourceAlreadyExistsError(DomainError):
    """Excepción cuando se intenta crear un recurso que ya existe."""
    pass


class ResourceNotFoundError(DomainError):
    """Excepción cuando no se encuentra un recurso."""
    pass


# ============================================================================
# Services (SRP: Cada servicio tiene una única responsabilidad)
# ============================================================================

class UsuarioService:
    """
    Servicio para gestión de usuarios.
    Responsabilidad: Orquestar operaciones del ciclo de vida de usuarios.
    """

    def __init__(self, usuario_repo: InMemoryUsuarioRepository):
        self.usuario_repo = usuario_repo

    def crear_usuario(self, cmd: CrearUsuarioCommand) -> Usuario:
        """
        Crea un nuevo usuario.
        
        Raises:
            ResourceAlreadyExistsError: Si el usuario ya existe.
        """
        # Verificar duplicados
        if self.usuario_repo.get(cmd.id):
            raise ResourceAlreadyExistsError(f"Usuario con id {cmd.id} ya existe.")

        # Crear entidad
        usuario = Usuario(
            id=cmd.id,
            nombre=cmd.nombre,
            email=cmd.email,
            apartamento=cmd.apartamento,
            telefono=cmd.telefono
        )

        # Persistir
        self.usuario_repo.add(usuario)

        return usuario

    def listar_usuarios(self) -> List[Usuario]:
        """Lista todos los usuarios."""
        return self.usuario_repo.list_all()


class UnidadResidencialService:
    """
    Servicio para gestión de unidades residenciales.
    Responsabilidad: Orquestar operaciones del ciclo de vida de unidades.
    """

    def __init__(self, unidad_repo: InMemoryUnidadResidencialRepository):
        self.unidad_repo = unidad_repo

    def crear_unidad(self, cmd: CrearUnidadResidencialCommand) -> UnidadResidencial:
        """
        Crea una nueva unidad residencial.
        
        Raises:
            ResourceAlreadyExistsError: Si la unidad ya existe.
        """
        if self.unidad_repo.get(cmd.id):
            raise ResourceAlreadyExistsError(f"Unidad con id {cmd.id} ya existe.")

        unidad = UnidadResidencial(
            id=cmd.id,
            nombre=cmd.nombre,
            direccion=cmd.direccion
        )

        self.unidad_repo.add(unidad)

        return unidad

    def listar_unidades(self) -> List[UnidadResidencial]:
        """Lista todas las unidades residenciales."""
        return self.unidad_repo.list_all()


class CategoriaService:
    """
    Servicio para gestión de categorías.
    Responsabilidad: Orquestar operaciones del ciclo de vida de categorías.
    """

    def __init__(self, categoria_repo: InMemoryCategoriaRepository):
        self.categoria_repo = categoria_repo

    def crear_categoria(self, cmd: CrearCategoriaCommand) -> Categoria:
        """
        Crea una nueva categoría.
        
        Raises:
            ResourceAlreadyExistsError: Si la categoría ya existe.
        """
        if self.categoria_repo.get(cmd.id):
            raise ResourceAlreadyExistsError(f"Categoría con id {cmd.id} ya existe.")

        categoria = Categoria(
            id=cmd.id,
            nombre=cmd.nombre,
            descripcion=cmd.descripcion
        )

        self.categoria_repo.add(categoria)

        return categoria

    def listar_categorias(self) -> List[Categoria]:
        """Lista todas las categorías."""
        return self.categoria_repo.list_all()


class PublicacionService:
    """
    Servicio para publicación de productos.
    Responsabilidad: Orquestar el flujo de publicación de productos.
    """

    def __init__(
        self,
        producto_repo: InMemoryProductoRepository,
        usuario_repo: InMemoryUsuarioRepository,
        categoria_repo: InMemoryCategoriaRepository,
        max_images: int = 4
    ):
        self.producto_repo = producto_repo
        self.usuario_repo = usuario_repo
        self.categoria_repo = categoria_repo
        self.max_images = max_images

    def publicar_producto(self, cmd: PublicarProductoCommand) -> Producto:
        """
        Publica un producto en el marketplace.
        
        Raises:
            ResourceNotFoundError: Si el vendedor o categoría no existen.
            PermissionError: Si el vendedor no tiene permisos.
            ValidationError: Si los datos del producto son inválidos.
        """
        # Buscar vendedor
        vendedor = self.usuario_repo.get(cmd.vendedor_id)
        if not vendedor:
            raise ResourceNotFoundError(f"Vendedor con id {cmd.vendedor_id} no encontrado.")

        # Buscar categoría
        categoria = self.categoria_repo.get(cmd.categoria_id)
        if not categoria:
            raise ResourceNotFoundError(f"Categoría con id {cmd.categoria_id} no encontrada.")

        # Verificar permisos
        if cmd.vendedor_status != "APPROVED":
            raise PermissionError("Solo usuarios APPROVED pueden publicar.")

        # Construir producto usando Builder (validaciones de dominio)
        builder = (
            ProductoBuilder(max_images=self.max_images)
            .vendedor(vendedor)
            .categoria(categoria)
            .nombre(cmd.nombre)
            .descripcion(cmd.descripcion)
            .precio_cop(cmd.precio_cop)
        )

        for url in cmd.imagenes[:self.max_images]:
            builder.add_imagen(url)

        producto = builder.build()

        # Persistir
        self.producto_repo.add(producto)

        # Notificar (side effect)
        notifier = NotifierFactory.create()
        notifier.notify_listing_created(vendedor.telefono, producto.nombre)

        return producto
