from django.contrib import admin
from .models import (
Make, CarModel, Generation, BodyType, FuelType, Transmission, DriveType, Color, Feature
)

for mdl in [Make, CarModel, Generation, BodyType, FuelType, Transmission, DriveType, Color, Feature]:
    @admin.register(mdl)
    class _Admin(admin.ModelAdmin):
        list_display = ("id", "__str__", "is_deleted")
        search_fields = ("name",)
        last_filter = ("is_deleted",)