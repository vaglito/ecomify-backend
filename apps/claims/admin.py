from django.contrib import admin
from django.utils import timezone
from .models import Claim

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'full_name', 'type', 'status', 'created_at')
    list_filter = ('status', 'type', 'created_at')
    search_fields = ('tracking_code', 'full_name', 'document_number')
    readonly_fields = ('tracking_code', 'created_at')
    
    fieldsets = (
        ("Seguimiento", {
            "fields": ("tracking_code", "status")
        }),
        ("Datos del Consumidor", {
            "fields": ("full_name", "document_type", "document_number", "email", "phone", "address", "district")
        }),
        ("Incidente", {
            "fields": ("type", "description", "amount_claimed", "file")
        }),
        ("Respuesta", {
            "fields": ("response", "response_date")
        }),
    )

    def save_model(self, request, obj, form, change):
        # Auto-set response date if response is added
        if obj.response and not obj.response_date:
            obj.response_date = timezone.now()
            obj.status = 'attended' 
        super().save_model(request, obj, form, change)
