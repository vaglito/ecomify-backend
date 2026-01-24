import os
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


def product_image_upload_path(instance, filename):
    # 'instance' será una instancia de ProductoImagen
    # El ID del producto se obtiene a través de la relación FK
    # Estructura: productos/id_123/nombre_archivo.jpg
    return f"productos/id_{instance.producto.id}/{filename}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_original = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    sku = models.CharField(max_length=50, unique=True)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="productos"
    )
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="productos")
    es_nuevo = models.BooleanField(default=True)
    en_oferta = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class ProductoImagen(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="imagenes"
    )
    imagen = models.ImageField(upload_to=product_image_upload_path)
    orden = models.IntegerField(
        default=0, help_text="Orden en que se mostrará en la galería"
    )

    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de productos"
        ordering = ["orden"]

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"


class Especificacion(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="especificaciones"
    )
    contenido = RichTextField()
    orden = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Especificación"
        verbose_name_plural = "Especificaciones"
        ordering = ["orden"]

    def __str__(self):
        return f"Especificación del producto {self.producto.nombre}"
