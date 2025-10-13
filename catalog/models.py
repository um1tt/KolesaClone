from django.db import models
from abstracts.models import TimeStampedModel, SoftDeleteModel


class Make(SoftDeleteModel, TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self):
        return self.name


class CarModel(SoftDeleteModel, TimeStampedModel):
    make = models.ForeignKey(Make, on_delete=models.PROTECT, related_name='models')
    name = models.CharField(max_length=120)
    class Meta:
        unique_together = ("make", "name")
    def __str__(self):
        return f"{self.make} {self.name}"


class Generation(SoftDeleteModel, TimeStampedModel):
    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT, related_name='generations')
    name = models.CharField(max_length=120) 
    years = models.CharField(max_length=64, blank=True) 
    class Meta:
        unique_together = ("car_model", "name")
    def __str__(self):
        return f"{self.car_model} {self.name}"



class BodyType(SoftDeleteModel, TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self):
        return self.name


class FuelType(SoftDeleteModel, TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self):
        return self.name


class Transmission(SoftDeleteModel, TimeStampedModel):
    name = models.CharField(max_length=80, unique=True) 
    def __str__(self):
        return self.name


class DriveType(SoftDeleteModel, TimeStampedModel):
    name = models.CharField(max_length=80, unique=True) 
    def __str__(self):
        return self.name


class Color(SoftDeleteModel, TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self):
        return self.name


class Feature(SoftDeleteModel, TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self):
        return self.name