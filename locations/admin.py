from django.contrib import admin
from .models import Region, City

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_deleted",
        "created_at", "updated_at")
    search_fields = ("name",)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "is_deleted",
        "created_at", "updated_at")
    list_filter = ("region",)
    search_fields = ("name",)