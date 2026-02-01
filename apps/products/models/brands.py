from django.db import models
from django.utils.text import slugify

def brand_image_upload_path(instance, filename):
    return f"brands/id_{instance.id}/{filename}"

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to=brand_image_upload_path, blank=True, null=True, verbose_name="Imagen")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
