"""
Puertos abstractos del dominio (Dependency Inversion Principle).
El dominio define interfaces; la infraestructura provee implementaciones concretas.
"""
from abc import ABC, abstractmethod


class DescriptionGeneratorPort(ABC):
    """Puerto para generación de descripciones con IA."""

    @abstractmethod
    def generar_descripcion(self, nombre_producto: str) -> str:
        """Genera una descripción profesional a partir del nombre del producto."""
        pass
