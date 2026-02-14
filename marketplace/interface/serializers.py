"""
Serializers - Solo validación de datos de entrada/salida.
Responsabilidad: Validar estructura de datos HTTP.
NO contiene lógica de negocio ni creación de entidades.
"""

from rest_framework import serializers


class UsuarioSerializer(serializers.Serializer):
    """Serializer para validación de datos de Usuario."""
    id = serializers.CharField(max_length=50)
    nombre = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    apartamento = serializers.CharField(max_length=20, required=False, allow_null=True)
    telefono = serializers.CharField(max_length=20, required=False, allow_null=True)


class UnidadResidencialSerializer(serializers.Serializer):
    """Serializer para validación de datos de Unidad Residencial."""
    id = serializers.CharField(max_length=50)
    nombre = serializers.CharField(max_length=100)
    direccion = serializers.CharField(max_length=200)


class CategoriaSerializer(serializers.Serializer):
    """Serializer para validación de datos de Categoría."""
    id = serializers.CharField(max_length=50)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField(max_length=200)


class ProductoSerializer(serializers.Serializer):
    """Serializer para salida de datos de Producto."""
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=100, read_only=True)
    precio = serializers.IntegerField(read_only=True)
    descripcion = serializers.CharField(read_only=True)
    stock = serializers.IntegerField(read_only=True)
    vendedor_id = serializers.CharField(source='vendedor.id', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)


class PublicarProductoSerializer(serializers.Serializer):
    """Serializer para validación de entrada al publicar un producto."""
    vendedor_id = serializers.CharField(max_length=50)
    vendedor_status = serializers.CharField(max_length=20)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    precio = serializers.IntegerField(min_value=1)
    categoria_id = serializers.CharField(max_length=50)
    imagenes = serializers.ListField(
        child=serializers.URLField(), 
        required=False, 
        default=list
    )
