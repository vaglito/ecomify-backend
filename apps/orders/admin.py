from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'id')
    readonly_fields = ('total_amount', 'created_at', 'user')
    inlines = [OrderItemInline]

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deleting orders for audit purposes
