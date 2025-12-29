from rest_framework.test import APITestCase
from rest_framework import status

from listings.models import Listing
from accounts.models import User
from locations.models import City, Region
from catalog.models import (
    Make, CarModel, BodyType, FuelType,
    Transmission, DriveType, Color
)

"это тест через APITest, вы сказали поменять, обновленные тесты через пайтест в фолдерах tests, а смысла удалять рабочий апитест не видел"

class ListingTests(APITestCase):
    """
    Тесты для объявлений (Listing).

    Проверяем:
    - создание объявления (успех и ошибки валидации)
    - обновление объявления (владелец / не владелец)
    - удаление объявления (владелец / не владелец)
    """

    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом:
        - создаём пользователя и авторизуем клиента
        - создаём справочники (регион/город, марка/модель и т.д.)
        - формируем валидный payload для создания объявления
        """
        self.user = User.objects.create_user(email="a@gmail.com", password="12345678")
        self.client.force_authenticate(user=self.user)

        region = Region.objects.create(name="Test Region")
        self.city = City.objects.create(name="Test City", region=region)

        self.make = Make.objects.create(name="Toyota")
        self.model = CarModel.objects.create(make=self.make, name="Camry")
        self.body = BodyType.objects.create(name="Sedan")
        self.fuel = FuelType.objects.create(name="Petrol")
        self.trans = Transmission.objects.create(name="AT")
        self.drive = DriveType.objects.create(name="FWD")
        self.color = Color.objects.create(name="Black")

        self.create_url = "/api/listings/create/"

        self.valid_data = {
            "city": self.city.id,
            "make": self.make.id,
            "car_model": self.model.id,
            "generation": None,
            "year": 2018,
            "mileage_km": 100000,
            "body_type": self.body.id,
            "fuel_type": self.fuel.id,
            "transmission": self.trans.id,
            "drive_type": self.drive.id,
            "color": self.color.id,
            "engine_volume_l": 2.5,
            "power_hp": 200,
            "steering_wheel": "left",
            "condition": "used",
            "vin": "VINTEST",
            "description": "Good car",
            "price_kzt": 5000000,
            "status": "published",
            "features": [],
            "contact_name": "Test",
            "contact_phone": "87770000000"
        }

    def test_create_listing_success(self):
        """
        Создание объявления с корректными данными.
        Ожидаем HTTP 201 CREATED.
        """
        response = self.client.post(self.create_url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_listing_missing_year(self):
        """
        Создание объявления без обязательного поля year.
        Ожидаем HTTP 400 BAD REQUEST.
        """
        invalid = self.valid_data.copy()
        del invalid["year"]

        response = self.client.post(self.create_url, invalid, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_listing_invalid_price(self):
        """
        Создание объявления с некорректной ценой (отрицательное значение).
        Ожидаем HTTP 400 BAD REQUEST.
        """
        invalid = self.valid_data.copy()
        invalid["price_kzt"] = -100

        response = self.client.post(self.create_url, invalid, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_listing_success(self):
        """
        Обновление объявления владельцем.
        Ожидаем HTTP 200 OK и обновлённое значение price_kzt.
        """
        listing = Listing.objects.create(
            user=self.user,
            city=self.city,
            make=self.make,
            car_model=self.model,
            body_type=self.body,
            fuel_type=self.fuel,
            transmission=self.trans,
            drive_type=self.drive,
            color=self.color,
            year=2018,
            mileage_km=100000,
            price_kzt=5000000
        )

        response = self.client.patch(
            f"/api/listings/{listing.id}/update/",
            {"price_kzt": 6000000},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price_kzt"], 6000000)

    def test_update_listing_not_owner(self):
        """
        Попытка обновить объявление НЕ владельцем.
        Ожидаем HTTP 403 FORBIDDEN.
        """
        other = User.objects.create_user(email="other@gmail.com", password="12345678")
        listing = Listing.objects.create(
            user=other,
            city=self.city,
            make=self.make,
            car_model=self.model,
            body_type=self.body,
            fuel_type=self.fuel,
            transmission=self.trans,
            drive_type=self.drive,
            color=self.color,
            year=2018,
            mileage_km=100000,
            price_kzt=5000000
        )

        response = self.client.patch(
            f"/api/listings/{listing.id}/update/",
            {"price_kzt": 7000000},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_listing_success(self):
        """
        Удаление объявления владельцем.
        Ожидаем HTTP 204 NO CONTENT.
        """
        listing = Listing.objects.create(
            user=self.user,
            city=self.city,
            make=self.make,
            car_model=self.model,
            body_type=self.body,
            fuel_type=self.fuel,
            transmission=self.trans,
            drive_type=self.drive,
            color=self.color,
            year=2018,
            mileage_km=100000,
            price_kzt=5000000
        )

        response = self.client.delete(f"/api/listings/{listing.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_listing_not_owner(self):
        """
        Попытка удалить объявление НЕ владельцем.
        Ожидаем HTTP 403 FORBIDDEN.
        """
        other = User.objects.create_user(email="other@gmail.com", password="12345678")
        listing = Listing.objects.create(
            user=other,
            city=self.city,
            make=self.make,
            car_model=self.model,
            body_type=self.body,
            fuel_type=self.fuel,
            transmission=self.trans,
            drive_type=self.drive,
            color=self.color,
            year=2018,
            mileage_km=100000,
            price_kzt=5000000
        )

        response = self.client.delete(f"/api/listings/{listing.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
