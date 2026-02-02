from django.db import models
from django.utils import timezone

class Claim(models.Model):
    DOCUMENT_TYPE_CHOICES = (
        ('DNI', 'DNI'),
        ('CE', 'Carnet de Extranjería'),
        ('RUC', 'RUC'),
        ('PASSPORT', 'Pasaporte'),
    )

    CLAIM_TYPE_CHOICES = (
        ('queja', 'Queja'),
        ('reclamo', 'Reclamo'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('attended', 'Atendido'),
        ('rejected', 'Rechazado'),
    )

    # Tracking
    tracking_code = models.CharField(max_length=20, unique=True, editable=False, verbose_name="Código de Seguimiento")
    
    # Personal Info
    full_name = models.CharField(max_length=255, verbose_name="Nombre Completo / Razón Social")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=50, verbose_name="Teléfono")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='DNI', verbose_name="Tipo de Documento")
    document_number = models.CharField(max_length=20, verbose_name="Número de Documento")
    
    # Address
    address = models.CharField(max_length=255, verbose_name="Dirección")
    district = models.CharField(max_length=100, verbose_name="Distrito")

    # Incident Details
    type = models.CharField(max_length=20, choices=CLAIM_TYPE_CHOICES, verbose_name="Tipo")
    description = models.TextField(verbose_name="Detalle del Reclamo/Queja")
    amount_claimed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Monto Reclamado")
    file = models.FileField(upload_to='claims/', null=True, blank=True, verbose_name="Adjunto (Evidencia)")

    # Status & Response
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    response = models.TextField(blank=True, null=True, verbose_name="Respuesta de la empresa")
    response_date = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Respuesta")

    class Meta:
        verbose_name = "Libro de Reclamaciones"
        verbose_name_plural = "Libro de Reclamaciones"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            # Generate code: REC-YYYY-XXXX (e.g., REC-2026-0001)
            year = timezone.now().year
            last_claim = Claim.objects.filter(created_at__year=year).count()
            self.tracking_code = f"REC-{year}-{last_claim + 1:04d}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_code} - {self.full_name}"
