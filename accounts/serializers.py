from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя.

    Отвечает за:
    - создание пользователя
    - валидацию email на уникальность
    - хеширование пароля
    - возврат JWT-токенов (access и refresh) после регистрации
    """

    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("email", "password", "phone")

    def validate_email(self, value):
        """
        Проверяет уникальность email.

        :param value: Email пользователя
        :raises ValidationError: если пользователь с таким email уже существует
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return value

    def create(self, validated_data):
        """
        Создаёт нового пользователя.

        Пароль хешируется с помощью set_password,
        чтобы не сохраняться в открытом виде.
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        """
        Переопределяет представление ответа.

        После успешной регистрации возвращает:
        - данные пользователя
        - JWT access и refresh токены
        """
        data = super().to_representation(instance)

        refresh = RefreshToken.for_user(instance)

        data["id"] = instance.id
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.

    Используется для получения и отображения данных пользователя.
    Email и id доступны только для чтения.
    """

    class Meta:
        model = User
        fields = ("id", "email", "phone", "first_name", "last_name")
        read_only_fields = ("id", "email")
