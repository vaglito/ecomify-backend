import os
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


def product_image_upload_path(instance, filename):
    # 'instance' will be an instance of ProductImage
    # The Product ID is obtained through the FK relation
    # Structure: products/id_123/filename.jpg
    return f"products/id_{instance.product.id}/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Precio"
    )
    original_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio Original"
    )
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="Categoría"
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products", verbose_name="Marca")
    is_new = models.BooleanField(default=True, verbose_name="Es Nuevo")
    on_sale = models.BooleanField(default=False, verbose_name="En Oferta")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="Producto"
    )
    image = models.ImageField(upload_to=product_image_upload_path, verbose_name="Imagen")
    order = models.IntegerField(
        default=0, help_text="Orden en que se mostrará en la galería", verbose_name="Orden"
    )

    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de productos"
        ordering = ["order"]

    def __str__(self):
        return f"Imagen de {self.product.name}"


class Specification(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications", verbose_name="Producto"
    )
    content = RichTextField(verbose_name="Contenido")
    order = models.IntegerField(default=0, verbose_name="Orden")

    class Meta:
        verbose_name = "Especificación"
        verbose_name_plural = "Especificaciones"
        ordering = ["order"]

    def __str__(self):
        return f"Especificación del producto {self.product.name}"
