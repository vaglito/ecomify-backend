from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'transaction_code', 'status', 'created_at', 'verified_by', 'preview_voucher')
    list_filter = ('status', 'created_at', 'verified_by')
    search_fields = ('transaction_code', 'order__id', 'order__user__username', 'order__user__email', 'order__user__first_name', 'order__user__last_name')
    readonly_fields = ('created_at', 'verified_at', 'verified_by', 'preview_voucher')
    actions = ['verify_payment', 'reject_payment']

    def preview_voucher(self, obj):
        if obj.payment_proof:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 100px; height: auto; border-radius: 4px;" /></a>',
                obj.payment_proof.url,
                obj.payment_proof.url
            )
        return "Sin voucher"
    preview_voucher.short_description = "Voucher"

    def save_model(self, request, obj, form, change):
        # Automated logic when saving a payment
        if change and 'status' in form.changed_data:
            if obj.status == 'verified':
                if not obj.verified_by:
                    obj.verified_by = request.user
                    obj.verified_at = timezone.now()
                
                # Automatically update order status to shipped (Enviado/Listo para Recoger)
                order = obj.order
                order.status = 'shipped'
                order.save()
                
            elif obj.status == 'rejected':
                 if not obj.verified_by:
                    obj.verified_by = request.user
                    obj.verified_at = timezone.now()

        super().save_model(request, obj, form, change)

    def verify_payment(self, request, queryset):
        # Update payments
        rows_updated = queryset.update(
            status='verified', 
            verified_at=timezone.now(), 
            verified_by=request.user
        )
        
        # Update associated orders
        for payment in queryset:
            order = payment.order
            order.status = 'shipped'
            order.save()
            
        self.message_user(request, f"{rows_updated} pagos verificados y órdenes marcadas como enviadas.")
    verify_payment.short_description = "Verificar pagos y marcar órdenes como enviadas"

    def reject_payment(self, request, queryset):
        rows_updated = queryset.update(
            status='rejected', 
            verified_at=timezone.now(), 
            verified_by=request.user
        )
        self.message_user(request, f"{rows_updated} pagos rechazados.")
    reject_payment.short_description = "Rechazar pagos seleccionados"
