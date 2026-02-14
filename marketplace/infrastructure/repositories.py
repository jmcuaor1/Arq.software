from typing import Optional, List
from ..domain.usuario import Usuario
from ..domain.categoria import Categoria
from ..domain.unidad_residencial import UnidadResidencial
from ..domain.producto import Producto

class InMemoryProductoRepository:
    def __init__(self):
        self.db = {}

    def add(self, producto: Producto):
        self.db[producto.id] = producto

    def get(self, id: str) -> Optional[Producto]:
        return self.db.get(id)

    def list_all(self) -> List[Producto]:
        return list(self.db.values())

class InMemoryUsuarioRepository:
    def __init__(self):
        self.db = {}

    def add(self, usuario: Usuario):
        self.db[usuario.id] = usuario

    def get(self, id: str) -> Optional[Usuario]:
        return self.db.get(id)

    def list_all(self) -> List[Usuario]:
        return list(self.db.values())

class InMemoryCategoriaRepository:
    def __init__(self):
        self.db = {}

    def add(self, categoria: Categoria):
        self.db[categoria.id] = categoria

    def get(self, id: str) -> Optional[Categoria]:
        return self.db.get(id)

    def list_all(self) -> List[Categoria]:
        return list(self.db.values())

class InMemoryUnidadResidencialRepository:
    def __init__(self):
        self.db = {}

    def add(self, unidad: UnidadResidencial):
        self.db[unidad.id] = unidad

    def get(self, id: str) -> Optional[UnidadResidencial]:
        return self.db.get(id)
    
    def list_all(self) -> List[UnidadResidencial]:
        return list(self.db.values())
