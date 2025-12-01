from django.contrib import admin
from .models import (
Make, CarModel, Generation, BodyType, FuelType, Transmission, DriveType, Color, Feature
)

for mdl in [Make, CarModel, Generation, BodyType, FuelType, Transmission, DriveType, Color, Feature]:
    @admin.register(mdl)
    class _Admin(admin.ModelAdmin):
        list_display = ("id", "__str__", "is_deleted",
        "created_at", "updated_at")
        search_fields = ("name",)
        list_filter = ("is_deleted",)