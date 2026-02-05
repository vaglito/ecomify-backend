from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active", "created_at")
    list_filter = ("is_staff", "is_active", "groups")
    search_fields = ("email", "first_name", "last_name", "phone")
    ordering = ("email",)
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    
    readonly_fields = ("created_at", "updated_at", "last_login")

    def save_model(self, request, obj, form, change):
        # Handle password hashing if changed directly (basic implementation)
        # For full security, use a proper form or UserAdmin with custom forms
        if not change or 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
