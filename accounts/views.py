from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(APIView):
    """
    Представление для регистрации пользователей.

    Принимает данные пользователя, выполняет валидацию
    и создаёт нового пользователя.
    После успешной регистрации возвращает данные пользователя
    и JWT-токены.
    """

    def post(self, request):
        """
        Обрабатывает POST-запрос на регистрацию пользователя.

        Ожидаемые данные:
        - email
        - password
        - phone (необязательно)

        :return: HTTP 201 CREATED и данные пользователя
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class MeView(APIView):
    """
    Представление для работы с профилем текущего пользователя.

    Доступно только для аутентифицированных пользователей.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Возвращает данные текущего авторизованного пользователя.

        :return: HTTP 200 OK и данные пользователя
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """
        Частично обновляет данные текущего пользователя.

        Обновляемые поля:
        - phone
        - first_name
        - last_name

        :return: HTTP 200 OK и обновлённые данные пользователя
        """
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
