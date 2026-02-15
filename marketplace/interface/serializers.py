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


class ServicioSerializer(serializers.Serializer):
    """Serializer para salida de datos de Servicio."""
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=100, read_only=True)
    precio = serializers.IntegerField(read_only=True)
    descripcion = serializers.CharField(read_only=True)
    disponible = serializers.BooleanField(read_only=True)
    proveedor_id = serializers.CharField(source='proveedor.id', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)


class PublicarServicioSerializer(serializers.Serializer):
    """Serializer para validación de entrada al publicar un servicio."""
    proveedor_id = serializers.CharField(max_length=50)
    proveedor_status = serializers.CharField(max_length=20)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    precio = serializers.IntegerField(min_value=1)
    categoria_id = serializers.CharField(max_length=50)


class ConsultaSerializer(serializers.Serializer):
    """Serializer para salida de datos de Consulta."""
    id = serializers.CharField(read_only=True)
    comprador_nombre = serializers.CharField(source='comprador.nombre', read_only=True)
    item_nombre = serializers.CharField(source='item.nombre', read_only=True)
    item_vendedor = serializers.SerializerMethodField()
    mensaje = serializers.CharField(read_only=True)
    estado = serializers.CharField(source='estado.value', read_only=True)
    fecha = serializers.DateTimeField(read_only=True)

    def get_item_vendedor(self, obj):
        if hasattr(obj.item, 'vendedor'):
            return obj.item.vendedor.nombre
        return obj.item.proveedor.nombre

class RegistrarConsultaSerializer(serializers.Serializer):
    """Serializer para entrada de datos de Consulta."""
    comprador_id = serializers.CharField(max_length=50)
    item_id = serializers.CharField(max_length=20)
    item_type = serializers.ChoiceField(choices=['producto', 'servicio'])
    mensaje = serializers.CharField(required=False, allow_blank=True, max_length=500)

