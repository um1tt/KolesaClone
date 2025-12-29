from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    Абстрактная базовая модель для хранения временных меток.

    Добавляет два поля:
    - created_at — дата и время создания объекта
    - updated_at — дата и время последнего обновления объекта
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(TimeStampedModel):
    """
    Абстрактная базовая модель с поддержкой «мягкого удаления» (soft delete).

    Объект не удаляется физически из базы данных.
    Вместо этого он помечается как удалённый:
    - is_deleted = True
    - deleted_at = дата и время удаления

    Наследует временные поля из TimeStampedModel.
    """

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        """
        Выполняет «мягкое удаление» объекта.

        Метод переопределяет стандартный delete():
        объект остаётся в базе данных, но помечается как удалённый.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    class Meta:
        abstract = True
