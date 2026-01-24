from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Marca, Producto, ProductoImagen, Especificacion

# --- INLINES ---
# Esto permite editar imágenes y specs dentro de la misma página del producto
admin.site.site_header = "Conexión DigitalJS - Administración"
admin.site.site_title = "Panel de Control Conexión DigitalJS"
admin.site.index_title = "Bienvenido al Gestor de E-commerce"


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 3  # Espacios vacíos para nuevas imágenes
    fields = ("imagen", "previsualizacion", "orden")
    readonly_fields = ("previsualizacion",)

    def previsualizacion(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="width: 50px; height: auto; border-radius: 4px;" />',
                obj.imagen.url,
            )
        return "Sin imagen"


class EspecificacionInline(admin.StackedInline):
    model = Especificacion
    extra = 1  # Espacios vacíos para specs
    fields = ("contenido", "orden")


# --- CONFIGURACIÓN DE MODELOS ---


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {
        "slug": ("nombre",)
    }  # Autocompleta el slug mientras escribes


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista general
    list_display = (
        "thumbnail",
        "nombre",
        "sku",
        "precio",
        "stock",
        "categoria",
        "marca",
        "en_oferta",
    )

    # Filtros laterales
    list_filter = ("categoria", "marca", "es_nuevo", "en_oferta", "fecha_creacion")

    # Buscador superior
    search_fields = ("nombre", "sku", "marca__nombre", "categoria__nombre")

    # Autocompletar slug
    prepopulated_fields = {"slug": ("nombre",)}

    # Permite editar el precio y stock directamente desde la lista sin entrar al producto
    list_editable = ("precio", "stock", "en_oferta")

    # Inyectamos las imágenes y las especificaciones
    inlines = [ProductoImagenInline, EspecificacionInline]

    # Función para mostrar la primera imagen del producto en la lista
    def thumbnail(self, obj):
        primera_imagen = obj.imagenes.first()
        if primera_imagen:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 4px;" />',
                primera_imagen.imagen.url,
            )
        return "—"

    thumbnail.short_description = "Vista"


# Opcional: Si quieres gestionar las imágenes por separado también
@admin.register(ProductoImagen)
class ProductoImagenAdmin(admin.ModelAdmin):
    list_display = ("producto", "previsualizacion", "orden")
    list_filter = ("producto",)

    def previsualizacion(self, obj):
        return format_html(
            '<img src="{}" style="width: 80px; height: auto;" />', obj.imagen.url
        )
