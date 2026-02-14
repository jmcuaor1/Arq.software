"""
Views - Capa de Presentación (Thin Controllers).
Responsabilidad: Validar entrada HTTP, delegar a servicios, mapear respuestas HTTP.
NO contiene lógica de negocio.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UsuarioSerializer, 
    UnidadResidencialSerializer, 
    CategoriaSerializer,
    ProductoSerializer, 
    PublicarProductoSerializer
)
from ..application.services import (
    UsuarioService,
    UnidadResidencialService,
    CategoriaService,
    PublicacionService,
    CrearUsuarioCommand,
    CrearUnidadResidencialCommand,
    CrearCategoriaCommand,
    PublicarProductoCommand,
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from ..domain.exceptions import DomainError, PermissionError
from ..infrastructure.repositories import (
    InMemoryProductoRepository, 
    InMemoryUsuarioRepository, 
    InMemoryCategoriaRepository, 
    InMemoryUnidadResidencialRepository
)

# ============================================================================
# Dependency Injection (repositorios y servicios globales)
# ============================================================================

_producto_repo = InMemoryProductoRepository()
_usuario_repo = InMemoryUsuarioRepository()
_categoria_repo = InMemoryCategoriaRepository()
_unidad_repo = InMemoryUnidadResidencialRepository()

# Servicios
_usuario_service = UsuarioService(_usuario_repo)
_unidad_service = UnidadResidencialService(_unidad_repo)
_categoria_service = CategoriaService(_categoria_repo)
_publicacion_service = PublicacionService(
    producto_repo=_producto_repo,
    usuario_repo=_usuario_repo,
    categoria_repo=_categoria_repo
)


# ============================================================================
# Views (Thin Controllers - Solo HTTP, sin lógica de negocio)
# ============================================================================

class UsuarioView(APIView):
    """
    Vista para gestión de usuarios.
    Responsabilidad: Validar HTTP y delegar a UsuarioService.
    """

    def get(self, request):
        """Lista todos los usuarios."""
        usuarios = _usuario_service.listar_usuarios()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Crea un nuevo usuario."""
        serializer = UsuarioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Delegar a servicio
            cmd = CrearUsuarioCommand(**serializer.validated_data)
            usuario = _usuario_service.crear_usuario(cmd)
            
            # Mapear respuesta
            return Response(
                UsuarioSerializer(usuario).data, 
                status=status.HTTP_201_CREATED
            )
        except ResourceAlreadyExistsError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)


class UnidadResidencialView(APIView):
    """
    Vista para gestión de unidades residenciales.
    Responsabilidad: Validar HTTP y delegar a UnidadResidencialService.
    """

    def get(self, request):
        """Lista todas las unidades."""
        unidades = _unidad_service.listar_unidades()
        serializer = UnidadResidencialSerializer(unidades, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Crea una nueva unidad residencial."""
        serializer = UnidadResidencialSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            cmd = CrearUnidadResidencialCommand(**serializer.validated_data)
            unidad = _unidad_service.crear_unidad(cmd)
            
            return Response(
                UnidadResidencialSerializer(unidad).data,
                status=status.HTTP_201_CREATED
            )
        except ResourceAlreadyExistsError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)


class CategoriaView(APIView):
    """
    Vista para gestión de categorías.
    Responsabilidad: Validar HTTP y delegar a CategoriaService.
    """

    def get(self, request):
        """Lista todas las categorías."""
        categorias = _categoria_service.listar_categorias()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Crea una nueva categoría."""
        serializer = CategoriaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            cmd = CrearCategoriaCommand(**serializer.validated_data)
            categoria = _categoria_service.crear_categoria(cmd)
            
            return Response(
                CategoriaSerializer(categoria).data,
                status=status.HTTP_201_CREATED
            )
        except ResourceAlreadyExistsError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)


class PublicarProductoView(APIView):
    """
    Vista para publicación de productos.
    Responsabilidad: Validar HTTP y delegar a PublicacionService.
    """

    def post(self, request):
        """Publica un producto."""
        serializer = PublicarProductoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Delegar a servicio (toda la lógica está en el servicio)
            # Mapear campos del serializer al comando
            cmd = PublicarProductoCommand(
                vendedor_id=serializer.validated_data['vendedor_id'],
                vendedor_status=serializer.validated_data['vendedor_status'],
                nombre=serializer.validated_data['nombre'],
                descripcion=serializer.validated_data['descripcion'],
                precio_cop=serializer.validated_data['precio'],  # Mapeo: precio -> precio_cop
                categoria_id=serializer.validated_data['categoria_id'],
                imagenes=serializer.validated_data.get('imagenes', [])
            )
            producto = _publicacion_service.publicar_producto(cmd)
            
            return Response(
                ProductoSerializer(producto).data,
                status=status.HTTP_201_CREATED
            )
        except ResourceNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except DomainError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Error interno del servidor."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
