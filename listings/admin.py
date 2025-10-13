from django.contrib import admin
from .models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "make", "car_model", "year", "city", "price_kzt", "status", "user")
    list_filter = (
        "status", "city", "make", "car_model", "year",
        "body_type", "fuel_type", "transmission", "drive_type", "color"
    )
    search_fields = ("vin", "description", "contact_phone", "user__username")
    autocomplete_fields = (
        "user", "city", "make", "car_model", "generation",
        "body_type", "fuel_type", "transmission", "drive_type",
        "color", "features"
    )