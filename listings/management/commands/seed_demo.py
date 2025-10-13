from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random

from locations.models import Region, City
from catalog.models import (
    Make, CarModel, Generation, BodyType, FuelType,
    Transmission, DriveType, Color, Feature
)
from listings.models import Listing, ListingStatus

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo data for Kolesa Clone"

    def handle(self, *args, **options):
        random.seed(42)

        # Users
        users = []
        for i in range(20):
            u, _ = User.objects.get_or_create(
                username=f'user{i}',
                defaults={"email": f"user{i}@ex.com"}
            )
            users.append(u)
        self.stdout.write(self.style.SUCCESS(f"Users: {len(users)}"))

        # Regions/Cities
        region_names = ["Атырауская", "Алматинская", "Мангистауская", "Западно-Казахстанская"]
        regions = [Region.objects.get_or_create(name=n)[0] for n in region_names]
        region_city_mapping = {
            "Атырауская": ["Атырау"],
            "Алматинская": ["Алматы"],
            "Мангистауская": ["Актау"],
            "Западно-Казахстанская": ["Уральск"],
        }

        cities = []
        for r in regions:
            for city_name in region_city_mapping[r.name]:
                city, _ = City.objects.get_or_create(region=r, name=city_name)
                cities.append(city)


        # Catalogs
        makes = [Make.objects.get_or_create(name=n)[0] for n in ["Toyota", "BMW", "Mercedes-Benz", "Hyundai", "LADA"]]
        car_models = []
        mapping = {
            "Toyota": ["Camry", "Corolla"],
            "BMW": ["5 Series", "3 Series"],
            "Mercedes-Benz": ["E-Class", "C-Class"],
            "Hyundai": ["Elantra", "Sonata"],
            "LADA": ["Vesta", "Granta"],
        }
        for m in makes:
            for mn in mapping[m.name]:
                car_models.append(CarModel.objects.get_or_create(make=m, name=mn)[0])

        generations = []
        for cm in car_models:
            for g in ["Gen1", "Gen2", "Gen3"]:
                generations.append(Generation.objects.get_or_create(car_model=cm, name=g)[0])

        body_types = [BodyType.objects.get_or_create(name=n)[0] for n in ["Sedan", "Hatchback", "SUV"]]
        fuel_types = [FuelType.objects.get_or_create(name=n)[0] for n in ["Petrol", "Diesel", "Hybrid"]]
        transmissions = [Transmission.objects.get_or_create(name=n)[0] for n in ["AT", "MT", "CVT"]]
        drive_types = [DriveType.objects.get_or_create(name=n)[0] for n in ["FWD", "RWD", "AWD"]]
        colors = [Color.objects.get_or_create(name=n)[0] for n in ["White", "Black", "Silver", "Blue", "Red"]]
        features = [Feature.objects.get_or_create(name=n)[0] for n in ["AC", "Heated seats", "Rear camera", "Cruise control", "Bluetooth"]]

        # Listings (>= 50)
        listings = []
        for i in range(50):
            cm = random.choice(car_models)
            l = Listing.objects.create(
                user=random.choice(users),
                city=random.choice(cities),
                make=cm.make,
                car_model=cm,
                generation=random.choice(generations),
                year=random.randint(2005, 2023),
                mileage_km=random.randint(10_000, 250_000),
                body_type=random.choice(body_types),
                fuel_type=random.choice(fuel_types),
                transmission=random.choice(transmissions),
                drive_type=random.choice(drive_types),
                color=random.choice(colors),
                engine_volume_l=random.choice([1.6, 1.8, 2.0, 2.5, 3.0]),
                power_hp=random.randint(90, 350),
                steering_wheel=random.choice(["left", "right"]),
                condition=random.choice(["new", "used"]),
                vin=f"VIN{100000+i}",
                description="Demo listing",
                price_kzt=random.randint(2_000_000, 35_000_000),
                status=random.choice([ListingStatus.DRAFT, ListingStatus.PUBLISHED]),
                contact_name=f"Seller {i}",
                contact_phone=f"+7 7{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
            )
            l.features.add(*random.sample(features, k=random.randint(1, len(features))))
            listings.append(l)

        self.stdout.write(self.style.SUCCESS(f"Listings: {len(listings)}"))
        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))