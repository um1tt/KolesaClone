from django.contrib import admin
from .models import Region, City

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_deleted")
    search_fields = ("name",)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "is_deleted")
    list_filter = ("region",)
    search_fields = ("name",)