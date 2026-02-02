from django.db import models

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, default="My E-commerce", verbose_name="Nombre del Sitio")
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Logo del Sitio")
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Favicon")
    
    contact_email = models.EmailField(verbose_name="Email de Contacto")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Teléfono")
    address = models.TextField(blank=True, null=True, verbose_name="Dirección")
    
    description = models.TextField(verbose_name="Descripción SEO (Meta)", help_text="Descripción corta para buscadores")

    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuración del Sitio"

    def save(self, *args, **kwargs):
        # Singleton logic: ensure only one ID=1 exists
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.site_name
