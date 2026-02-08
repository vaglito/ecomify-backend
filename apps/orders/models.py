from django.db import models
from django.conf import settings
from apps.products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="Usuario")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    shipping_address = models.TextField(verbose_name="Dirección de Envío")
    phone = models.CharField(max_length=20, verbose_name="Teléfono de Contacto")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"
        ordering = ['-created_at']

    def __str__(self):
        try:
            return f"Orden #{self.id} - {self.user}"
        except Exception:
            return f"Orden #{self.id} (Usuario no encontrado)"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Orden")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")

    class Meta:
        verbose_name = "Item de Orden"
        verbose_name_plural = "Items de Orden"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
