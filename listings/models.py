from django.db import models
from django.conf import settings
from abstracts.models import TimeStampedModel, SoftDeleteModel
from locations.models import City
from catalog.models import (
    Make, CarModel, Generation, BodyType, FuelType,
    Transmission, DriveType, Color, Feature
)


class ListingStatus(models.TextChoices):
    """
    Статусы объявления.
    """
    DRAFT = "draft", "Черновик"
    PUBLISHED = "published", "Опубликовано"
    SOLD = "sold", "Продано"


class SteeringWheel(models.TextChoices):
    """
    Расположение рулевого колеса.
    """
    LEFT = "left", "Левый руль"
    RIGHT = "right", "Правый руль"


class Condition(models.TextChoices):
    """
    Состояние автомобиля.
    """
    NEW = "new", "Новый"
    USED = "used", "Б/у"


class Listing(SoftDeleteModel, TimeStampedModel):
    """
    Объявление о продаже автомобиля.

    Содержит полную информацию об автомобиле,
    его технических характеристиках, цене,
    местоположении и контактных данных продавца.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
        help_text="Владелец объявления"
    )

    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="listings",
        help_text="Город размещения объявления"
    )

    make = models.ForeignKey(
        Make,
        on_delete=models.PROTECT,
        help_text="Марка автомобиля"
    )
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.PROTECT,
        help_text="Модель автомобиля"
    )
    generation = models.ForeignKey(
        Generation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Поколение модели"
    )

    year = models.PositiveIntegerField(
        help_text="Год выпуска автомобиля"
    )
    mileage_km = models.PositiveIntegerField(
        default=0,
        help_text="Пробег в километрах"
    )

    body_type = models.ForeignKey(
        BodyType,
        on_delete=models.PROTECT,
        help_text="Тип кузова"
    )
    fuel_type = models.ForeignKey(
        FuelType,
        on_delete=models.PROTECT,
        help_text="Тип топлива"
    )
    transmission = models.ForeignKey(
        Transmission,
        on_delete=models.PROTECT,
        help_text="Тип коробки передач"
    )
    drive_type = models.ForeignKey(
        DriveType,
        on_delete=models.PROTECT,
        help_text="Тип привода"
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        help_text="Цвет автомобиля"
    )

    engine_volume_l = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Объём двигателя (литры)"
    )
    power_hp = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Мощность двигателя (л.с.)"
    )

    steering_wheel = models.CharField(
        max_length=8,
        choices=SteeringWheel.choices,
        default=SteeringWheel.LEFT,
        help_text="Расположение рулевого колеса"
    )
    condition = models.CharField(
        max_length=8,
        choices=Condition.choices,
        default=Condition.USED,
        help_text="Состояние автомобиля"
    )

    vin = models.CharField(
        max_length=32,
        blank=True,
        help_text="VIN-код автомобиля"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание автомобиля"
    )

    price_kzt = models.PositiveIntegerField(
        help_text="Цена в тенге"
    )

    status = models.CharField(
        max_length=12,
        choices=ListingStatus.choices,
        default=ListingStatus.DRAFT,
        help_text="Статус объявления"
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Дата публикации объявления"
    )

    features = models.ManyToManyField(
        Feature,
        blank=True,
        related_name="listings",
        help_text="Дополнительные опции автомобиля"
    )

    contact_name = models.CharField(
        max_length=120,
        blank=True,
        help_text="Контактное имя продавца"
    )
    contact_phone = models.CharField(
        max_length=64,
        blank=True,
        help_text="Контактный телефон продавца"
    )

    class Meta:
        """
        Дополнительные настройки модели.
        """
        indexes = [
            models.Index(fields=["status", "city", "make", "car_model"]),
        ]

    def __str__(self):
        """
        Человекочитаемое представление объявления.
        """
        return f"{self.make} {self.car_model} {self.year} — {self.price_kzt} KZT"
