from django.contrib import admin
from django.utils.html import format_html
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'transaction_code', 'status', 'created_at', 'preview_voucher')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_code', 'order__id', 'order__user__username')
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

    def verify_payment(self, request, queryset):
        rows_updated = queryset.update(status='verified', verified_at=admin.options.timezone.now(), verified_by=request.user)
        # Here we could also update the Order status to 'Paid' or 'Processing'
        for payment in queryset:
            order = payment.order
            order.status = 'processing' # Or 'shipped' depending on workflow
            order.save()
            
        self.message_user(request, f"{rows_updated} pagos verificados.")
    verify_payment.short_description = "Verificar pagos seleccionados"

    def reject_payment(self, request, queryset):
        rows_updated = queryset.update(status='rejected', verified_at=admin.options.timezone.now(), verified_by=request.user)
        self.message_user(request, f"{rows_updated} pagos rechazados.")
    reject_payment.short_description = "Rechazar pagos seleccionados"
