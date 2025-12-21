import pytest
from rest_framework.test import APIClient
from accounts.models import User
from listings.models import Listing
from locations.models import City, Region
from catalog.models import (
    Make, CarModel, BodyType, FuelType,
    Transmission, DriveType, Color
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="user@gmail.com",
        password="12345678"
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def listing_data():
    region = Region.objects.create(name="Region")
    city = City.objects.create(name="City", region=region)

    make = Make.objects.create(name="Toyota")
    model = CarModel.objects.create(make=make, name="Camry")
    body = BodyType.objects.create(name="Sedan")
    fuel = FuelType.objects.create(name="Petrol")
    trans = Transmission.objects.create(name="AT")
    drive = DriveType.objects.create(name="FWD")
    color = Color.objects.create(name="Black")

    return {
        "city": city.id,
        "make": make.id,
        "car_model": model.id,
        "generation": None,
        "year": 2018,
        "mileage_km": 100000,
        "body_type": body.id,
        "fuel_type": fuel.id,
        "transmission": trans.id,
        "drive_type": drive.id,
        "color": color.id,
        "engine_volume_l": 2.0,
        "power_hp": 150,
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


@pytest.mark.django_db
def test_create_listing_success(auth_client, listing_data):
    response = auth_client.post(
        "/api/listings/create/",
        listing_data,
        format="json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_listing_missing_year(auth_client, listing_data):
    listing_data.pop("year")

    response = auth_client.post(
        "/api/listings/create/",
        listing_data,
        format="json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_update_listing_not_owner(auth_client, listing_data):
    other = User.objects.create_user(
        email="other@gmail.com",
        password="12345678"
    )

    listing = Listing.objects.create(
        user=other,
        city_id=listing_data["city"],
        make_id=listing_data["make"],
        car_model_id=listing_data["car_model"],
        body_type_id=listing_data["body_type"],
        fuel_type_id=listing_data["fuel_type"],
        transmission_id=listing_data["transmission"],
        drive_type_id=listing_data["drive_type"],
        color_id=listing_data["color"],
        year=2018,
        mileage_km=100000,
        price_kzt=5000000
    )

    response = auth_client.patch(
        f"/api/listings/{listing.id}/update/",
        {"price_kzt": 7000000},
        format="json"
    )

    assert response.status_code == 403
