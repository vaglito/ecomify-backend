from rest_framework import serializers
from .models import Producto, Categoria, Marca, ProductoImagen, Especificacion


# 1. Serializador de Categorías
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "slug"]


# 2. Serializador de Marcas
class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ["id", "nombre", "slug"]


# 3. Serializador de la Galería de Imágenes
class ProductoImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
        fields = ["id", "imagen", "orden"]


# 4. Serializador de Especificaciones Técnicas (Clave-Valor)
class EspecificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especificacion
        fields = ["id", "titulo", "valor", "orden"]


# 5. Serializador Principal de Producto
class ProductoSerializer(serializers.ModelSerializer):
    # Relaciones anidadas (leídas de los modelos relacionados)
    imagenes = ProductoImagenSerializer(many=True, read_only=True)
    especificaciones = EspecificacionSerializer(many=True, read_only=True)

    # Campos de solo lectura para mostrar nombres en lugar de IDs
    categoria_nombre = serializers.ReadOnlyField(source="categoria.nombre")
    marca_nombre = serializers.ReadOnlyField(source="marca.nombre")

    # Cálculo dinámico del porcentaje de descuento para el frontend
    descuento_porcentaje = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "slug",
            "descripcion",
            "precio",
            "precio_original",
            "descuento_porcentaje",
            "sku",
            "stock",
            "es_nuevo",
            "en_oferta",
            "categoria",
            "categoria_nombre",
            "marca",
            "marca_nombre",
            "imagenes",
            "especificaciones",
            "fecha_creacion",
        ]

    def get_descuento_porcentaje(self, obj):
        if obj.precio_original and obj.precio_original > obj.precio:
            descuento = ((obj.originalPrice - obj.price) / obj.originalPrice) * 100
            return round(descuento)
        return 0
