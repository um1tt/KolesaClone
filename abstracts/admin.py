from django.contrib import admin
class SoftDeleteAdminMixin:
    list_filter = ("is_deleted",)
    readonly_fields = ("created_at", "updated_at") if hasattr(admin.ModelAdmin, 'created_at') else ()

