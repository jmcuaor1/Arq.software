"""Usuario/Residente del marketplace con validaciones de negocio."""

import re
from dataclasses import dataclass
from typing import Optional

from .exceptions import ValidationError


@dataclass
class Usuario:
    """
    Residente que puede vender productos, ofrecer servicios y comprar.
    
    Validaciones de negocio:
    - Nombre: no vacío, 2-100 caracteres
    - Email: formato válido
    - Teléfono: 10 dígitos (opcional)
    - Apartamento: máximo 20 caracteres (opcional)
    """

    id: str
    nombre: str
    email: str
    apartamento: Optional[str] = None
    telefono: Optional[str] = None

    def __post_init__(self):
        """Validar invariantes de negocio."""
        # Validar ID
        if not self.id or not self.id.strip():
            raise ValidationError("El ID del usuario no puede estar vacío.")

        # Validar nombre
        if not self.nombre or not self.nombre.strip():
            raise ValidationError("El nombre del usuario no puede estar vacío.")
        
        nombre_limpio = self.nombre.strip()
        if len(nombre_limpio) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres.")
        if len(nombre_limpio) > 100:
            raise ValidationError("El nombre no puede exceder 100 caracteres.")
        
        # Normalizar nombre
        self.nombre = nombre_limpio

        # Validar email
        if not self.email or not self.email.strip():
            raise ValidationError("El email no puede estar vacío.")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email.strip()):
            raise ValidationError(f"Email inválido: {self.email}")
        
        # Normalizar email
        self.email = self.email.strip().lower()

        # Validar teléfono (opcional)
        if self.telefono is not None:
            telefono_limpio = self.telefono.strip()
            # Remover caracteres no numéricos
            telefono_numeros = re.sub(r'\D', '', telefono_limpio)
            
            if len(telefono_numeros) != 10:
                raise ValidationError(
                    f"El teléfono debe tener exactamente 10 dígitos. Recibido: {telefono_limpio}"
                )
            
            # Normalizar teléfono
            self.telefono = telefono_numeros

        # Validar apartamento (opcional)
        if self.apartamento is not None:
            apto_limpio = self.apartamento.strip()
            if len(apto_limpio) > 20:
                raise ValidationError("El apartamento no puede exceder 20 caracteres.")
            
            # Normalizar apartamento
            self.apartamento = apto_limpio if apto_limpio else None

    def __str__(self) -> str:
        return f"{self.nombre} ({self.apartamento or 'Sin apto'})"
