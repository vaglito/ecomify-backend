from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Product, ProductImage, Specification

# --- INLINES ---
# Esto permite editar imágenes y specs dentro de la misma página del producto
admin.site.site_header = "Conexión DigitalJS - Administración"
admin.site.site_title = "Panel de Control Conexión DigitalJS"
admin.site.index_title = "Bienvenido al Gestor de E-commerce"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Empty spaces for new images
    fields = ("image", "preview", "order")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: auto; border-radius: 4px;" />',
                obj.image.url,
            )
        return "Sin imagen"


class SpecificationInline(admin.StackedInline):
    model = Specification
    extra = 1  # Empty spaces for specs
    fields = ("content", "order")


# --- CONFIGURACIÓN DE MODELOS ---


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {
        "slug": ("name",)
    }  # Autocompletes slug while typing


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columns visible in the general list
    list_display = (
        "thumbnail",
        "name",
        "sku",
        "price",
        "stock",
        "category",
        "brand",
        "on_sale",
    )

    # Sidebar filters
    list_filter = ("category", "brand", "is_new", "on_sale", "created_at")

    # Top search bar
    search_fields = ("name", "sku", "brand__name", "category__name")

    # Autocomplete slug
    prepopulated_fields = {"slug": ("name",)}

    # Allows editing price and stock directly from the list
    list_editable = ("price", "stock", "on_sale")

    # Inject images and specifications
    inlines = [ProductImageInline, SpecificationInline]

    # Function to show the first image of the product in the list
    def thumbnail(self, obj):
        first_image = obj.images.first()
        if first_image:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 4px;" />',
                first_image.image.url,
            )
        return "—"

    thumbnail.short_description = "Vista"


# Optional: If you want to manage images separately
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "preview", "order")
    list_filter = ("product",)

    def preview(self, obj):
        return format_html(
            '<img src="{}" style="width: 80px; height: auto;" />', obj.image.url
        )
