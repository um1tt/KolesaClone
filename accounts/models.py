from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей.

    Отвечает за создание обычных пользователей и суперпользователей
    с использованием email в качестве основного идентификатора.
    """

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет обычного пользователя.

        :param email: Email пользователя (обязателен)
        :param password: Пароль пользователя
        :param extra_fields: Дополнительные поля модели User
        :return: Объект пользователя
        """
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет суперпользователя.

        Автоматически устанавливает:
        - is_staff = True
        - is_superuser = True
        - is_active = True
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомная модель пользователя.

    Особенности:
    - В качестве логина используется email
    - Поле username отключено
    - Добавлено поле phone
    """

    username = None
    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        unique=True,
        help_text="Номер телефона пользователя"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """
        Строковое представление пользователя.
        """
        return self.email
