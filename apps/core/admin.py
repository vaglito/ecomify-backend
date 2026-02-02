from django.contrib import admin
from .models import SiteSetting

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    # Restrict permissions to enforce Singleton behavior
    def has_add_permission(self, request):
        # Allow add only if no record exists
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False
