from django.db import models
from .products import Product

class ProductStatistics(models.Model):
    product = models.OneToOneField(
        Product, 
        on_delete=models.CASCADE, 
        related_name="statistics",
        verbose_name="Producto"
    )
    visits = models.PositiveIntegerField(default=0, verbose_name="Visitas")
    sales = models.PositiveIntegerField(default=0, verbose_name="Ventas")
    last_visit = models.DateTimeField(auto_now=True, verbose_name="Última Visita")

    class Meta:
        verbose_name = "Estadística de Producto"
        verbose_name_plural = "Estadísticas de Productos"

    def __str__(self):
        return f"Estadísticas de {self.product.name}"
