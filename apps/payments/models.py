from django.db import models
from django.conf import settings
from apps.orders.models import Order

def payment_proof_upload_path(instance, filename):
    return f"payments/order_{instance.order.id}/{filename}"

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente de Verificación'),
        ('verified', 'Verificado'),
        ('rejected', 'Rechazado'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment', verbose_name="Orden")
    transaction_code = models.CharField(max_length=50, verbose_name="Código de Operación")
    payment_proof = models.ImageField(upload_to=payment_proof_upload_path, verbose_name="Comprobante de Pago (Voucher)")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Verificación")
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='verified_payments',
        verbose_name="Verificado Por"
    )

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-created_at']

    def __str__(self):
        return f"Pago {self.transaction_code} - Orden #{self.order.id}"
