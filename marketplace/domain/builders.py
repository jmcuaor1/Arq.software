import uuid
from decimal import Decimal
from dataclasses import replace
from .exceptions import ValidationError
from .producto import Producto
from .usuario import Usuario
from .categoria import Categoria

class ProductoBuilder:
    """
    Builder para crear productos con validaciones.
    
    Nota: Las validaciones principales están en la entidad Producto.
    Este builder solo valida reglas de negocio específicas del proceso de publicación.
    """
    
    def __init__(self, max_images: int = 4):
        self.max_images = max_images
        self._vendedor: Usuario | None = None
        self._categoria: Categoria | None = None
        self._nombre: str | None = None
        self._descripcion: str | None = None
        self._precio_cop: int | None = None
        self._imagenes: list[str] = []

    def vendedor(self, u: Usuario):
        self._vendedor = u
        return self

    def categoria(self, c: Categoria):
        self._categoria = c
        return self

    def nombre(self, nombre: str):
        self._nombre = (nombre or "").strip()
        return self

    def descripcion(self, descripcion: str):
        self._descripcion = (descripcion or "").strip()
        return self

    def precio_cop(self, precio: int):
        """
        Establece el precio en COP.
        Validación de rango de negocio: 1.000 - 50.000.000 COP.
        """
        self._precio_cop = int(precio)
        return self

    def add_imagen(self, url: str):
        url = (url or "").strip()
        if not url:
            raise ValidationError("La URL de la imagen no puede estar vacía.")
        if len(self._imagenes) >= self.max_images:
            raise ValidationError(f"Máximo {self.max_images} imágenes.")
        self._imagenes.append(url)
        return self

    def build(self) -> Producto:
        """
        Construye el producto.
        Valida reglas de negocio específicas de publicación antes de crear la entidad.
        """
        if self._vendedor is None:
            raise ValidationError("Vendedor requerido.")
        if self._categoria is None:
            raise ValidationError("Categoría requerida.")
        if not self._nombre or not (5 <= len(self._nombre) <= 60):
            raise ValidationError("Nombre debe tener 5-60 caracteres.")
        if not self._descripcion or not (20 <= len(self._descripcion) <= 500):
            raise ValidationError("Descripción debe tener 20-500 caracteres.")
        if self._precio_cop is None or not (1_000 <= self._precio_cop <= 50_000_000):
            raise ValidationError("Precio COP debe estar entre 1.000 y 50.000.000.")

        # Convertir precio a Decimal
        precio_decimal = Decimal(str(self._precio_cop))

        # Crear producto (las validaciones de la entidad se ejecutarán en __post_init__)
        return Producto(
            id=str(uuid.uuid4()),
            nombre=self._nombre,
            descripcion=self._descripcion,
            precio=precio_decimal,  # Usar Decimal
            vendedor=self._vendedor,
            categoria=self._categoria,
            imagenes=list(self._imagenes),
        )
