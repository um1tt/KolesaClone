from django.db import models
from django.conf import settings
from abstracts.models import TimeStampedModel, SoftDeleteModel
from locations.models import City
from catalog.models import (
    Make, CarModel, Generation, BodyType, FuelType,
    Transmission, DriveType, Color, Feature
)


class ListingStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    SOLD = 'sold', 'Sold'


class SteeringWheel(models.TextChoices):
    LEFT = 'left', 'Left'
    RIGHT = 'right', 'Right'


class Condition(models.TextChoices):
    NEW = 'new', 'New'
    USED = 'used', 'Used'


class Listing(SoftDeleteModel, TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings'
    )
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='listings')

    make = models.ForeignKey(Make, on_delete=models.PROTECT)
    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    generation = models.ForeignKey(Generation, on_delete=models.SET_NULL, null=True, blank=True)

    year = models.PositiveIntegerField()
    mileage_km = models.PositiveIntegerField(default=0)

    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.PROTECT)
    transmission = models.ForeignKey(Transmission, on_delete=models.PROTECT)
    drive_type = models.ForeignKey(DriveType, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)

    engine_volume_l = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    power_hp = models.PositiveIntegerField(null=True, blank=True)

    steering_wheel = models.CharField(
        max_length=8, choices=SteeringWheel.choices, default=SteeringWheel.LEFT
    )
    condition = models.CharField(
        max_length=8, choices=Condition.choices, default=Condition.USED
    )

    vin = models.CharField(max_length=32, blank=True)
    description = models.TextField(blank=True)

    price_kzt = models.PositiveIntegerField()
    status = models.CharField(
        max_length=12, choices=ListingStatus.choices, default=ListingStatus.DRAFT
    )
    published_at = models.DateTimeField(null=True, blank=True)

    features = models.ManyToManyField(Feature, blank=True, related_name='listings')

    contact_name = models.CharField(max_length=120, blank=True)
    contact_phone = models.CharField(max_length=64, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "city", "make", "car_model"]),
        ]

    def __str__(self):
        return f"{self.make} {self.car_model} {self.year} — {self.price_kzt} KZT"