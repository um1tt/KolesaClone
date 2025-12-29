from django.db import models
from abstracts.models import TimeStampedModel, SoftDeleteModel


class Region(SoftDeleteModel, TimeStampedModel):
    """
    Регион (область, штат, край).

    Используется для группировки городов.
    Пример:
    - Алматинская область
    - Астана
    """

    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class City(SoftDeleteModel, TimeStampedModel):
    """
    Город, относящийся к конкретному региону.

    Уникальность города обеспечивается в пределах одного региона.
    Пример:
    - Алматы (Алматинская область)
    - Атырау (Атырауская область)
    """

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="cities"
    )
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("region", "name")

    def __str__(self):
        return f"{self.name} ({self.region.name})"
