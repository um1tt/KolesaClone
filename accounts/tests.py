from rest_framework.test import APITestCase
from accounts.models import User
from rest_framework import status


class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.me_url = "/api/users/me/"

    def test_register_success(self):
        data = {
            "email": "test@gmail.com",
            "password": "12345678",
            "phone": "87770000000"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_register_missing_email(self):
        response = self.client.post(
            self.register_url,
            {"password": "12345678"},
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_email(self):
        response = self.client.post(
            self.register_url,
            {"email": "wrong", "password": "12345678"},
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_register_existing_email(self):
        User.objects.create_user(email="duplicate@gmail.com", password="123456")
        response = self.client.post(
            self.register_url,
            {"email": "duplicate@gmail.com", "password": "123456"},
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_login_success(self):
        User.objects.create_user(email="login@gmail.com", password="12345678")
        response = self.client.post(
            self.login_url,
            {"email": "login@gmail.com", "password": "12345678"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_login_wrong_password(self):
        User.objects.create_user(email="login2@gmail.com", password="12345678")
        response = self.client.post(
            self.login_url,
            {"email": "login2@gmail.com", "password": "wrongpass"},
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_login_no_email(self):
        response = self.client.post(
            self.login_url,
            {"password": "123456"},
            format='json'
        )
        self.assertEqual(response.status_code, 400)


    def test_me_unauthorized(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, 401)

    def test_me_success(self):
        user = User.objects.create_user(email="me@gmail.com", password="12345678")
        self.client.force_authenticate(user=user)

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "me@gmail.com")
