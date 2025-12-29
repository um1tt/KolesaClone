from rest_framework.test import APITestCase
from accounts.models import User
from rest_framework import status

"это тест через APITest, вы сказали поменять, обновленные тесты через пайтест в фолдерах tests, а смысла удалять рабочий апитест не видел"

class AuthTests(APITestCase):
    """
    Тесты для модуля аутентификации и профиля пользователя.

    Проверяем:
    - регистрацию (успех и ошибки валидации)
    - логин (успех и неверные данные)
    - доступ к эндпоинту /me (без авторизации и с авторизацией)
    """

    def setUp(self):
        """
        Подготовка базовых URL для тестов.
        Вызывается перед каждым тестом.
        """
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.me_url = "/api/users/me/"

    def test_register_success(self):
        """
        Регистрация должна проходить успешно при корректных данных.
        Ожидаем HTTP 201 CREATED.
        """
        data = {
            "email": "test@gmail.com",
            "password": "12345678",
            "phone": "87770000000"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_missing_email(self):
        """
        Регистрация должна возвращать ошибку, если email не передан.
        Ожидаем HTTP 400 BAD REQUEST.
        """
        response = self.client.post(
            self.register_url,
            {"password": "12345678"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_email(self):
        """
        Регистрация должна возвращать ошибку, если email некорректный.
        Ожидаем HTTP 400 BAD REQUEST.
        """
        response = self.client.post(
            self.register_url,
            {"email": "wrong", "password": "12345678"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_existing_email(self):
        """
        Регистрация должна возвращать ошибку, если email уже существует.
        Ожидаем HTTP 400 BAD REQUEST.
        """
        User.objects.create_user(email="duplicate@gmail.com", password="123456")
        response = self.client.post(
            self.register_url,
            {"email": "duplicate@gmail.com", "password": "123456"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """
        Логин должен проходить успешно при корректных данных.
        Ожидаем HTTP 200 OK.
        """
        User.objects.create_user(email="login@gmail.com", password="12345678")
        response = self.client.post(
            self.login_url,
            {"email": "login@gmail.com", "password": "12345678"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_password(self):
        """
        Логин должен возвращать ошибку при неверном пароле.
        Ожидаем HTTP 401 UNAUTHORIZED.
        """
        User.objects.create_user(email="login2@gmail.com", password="12345678")
        response = self.client.post(
            self.login_url,
            {"email": "login2@gmail.com", "password": "wrongpass"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_no_email(self):
        """
        Логин должен возвращать ошибку, если email не передан.
        Ожидаем HTTP 400 BAD REQUEST.
        """
        response = self.client.post(
            self.login_url,
            {"password": "123456"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_me_unauthorized(self):
        """
        /me должен быть недоступен без авторизации.
        Ожидаем HTTP 401 UNAUTHORIZED.
        """
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_success(self):
        """
        /me должен возвращать данные текущего пользователя при авторизации.
        Ожидаем HTTP 200 OK и корректный email в ответе.
        """
        user = User.objects.create_user(email="me@gmail.com", password="12345678")
        self.client.force_authenticate(user=user)

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "me@gmail.com")
