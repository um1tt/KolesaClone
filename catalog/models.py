from django.db import models
from abstracts.models import TimeStampedModel, SoftDeleteModel


class Make(SoftDeleteModel, TimeStampedModel):
    """
    Марка автомобиля (производитель).

    Пример:
    - Toyota
    - BMW
    - Mercedes-Benz
    """

    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class CarModel(SoftDeleteModel, TimeStampedModel):
    """
    Модель автомобиля, относящаяся к конкретной марке.

    Пример:
    - Toyota Camry
    - BMW 5 Series

    Уникальность обеспечивается парой (make, name).
    """

    make = models.ForeignKey(
        Make,
        on_delete=models.PROTECT,
        related_name="models"
    )
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("make", "name")

    def __str__(self):
        return f"{self.make} {self.name}"


class Generation(SoftDeleteModel, TimeStampedModel):
    """
    Поколение модели автомобиля.

    Пример:
    - Camry XV50 (2011–2017)
    - BMW G30 (2017–2023)

    Уникальность обеспечивается парой (car_model, name).
    """

    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.PROTECT,
        related_name="generations"
    )
    name = models.CharField(max_length=120)
    years = models.CharField(
        max_length=64,
        blank=True,
        help_text="Годы выпуска поколения"
    )

    class Meta:
        unique_together = ("car_model", "name")

    def __str__(self):
        return f"{self.car_model} {self.name}"


class BodyType(SoftDeleteModel, TimeStampedModel):
    """
    Тип кузова автомобиля.

    Пример:
    - Седан
    - Хэтчбек
    - Кроссовер
    """

    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class FuelType(SoftDeleteModel, TimeStampedModel):
    """
    Тип топлива автомобиля.

    Пример:
    - Бензин
    - Дизель
    - Электро
    """

    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Transmission(SoftDeleteModel, TimeStampedModel):
    """
    Тип коробки передач.

    Пример:
    - Механика
    - Автомат
    - Вариатор
    """

    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class DriveType(SoftDeleteModel, TimeStampedModel):
    """
    Тип привода автомобиля.

    Пример:
    - Передний
    - Задний
    - Полный
    """

    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Color(SoftDeleteModel, TimeStampedModel):
    """
    Цвет автомобиля.
    """

    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Feature(SoftDeleteModel, TimeStampedModel):
    """
    Дополнительная опция / характеристика автомобиля.

    Пример:
    - Климат-контроль
    - Круиз-контроль
    - Панорамная крыша
    """

    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name
