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
    help = "Seed demo data for KolesaClone (updated version)"

    def handle(self, *args, **options):
        random.seed(42)

        users = []
        for i in range(20):
            email = f"user{i}@example.com"
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "password": "12345678",
                    "phone": f"87000000{i:02d}"
                }
            )
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f"Users created: {len(users)}"))

        region_data = {
            "Атырауская": ["Атырау"],
            "Алматинская": ["Алматы"],
            "Мангистауская": ["Актау"],
            "Западно-Казахстанская": ["Уральск"],
        }

        regions = []
        cities = []

        for region_name, city_list in region_data.items():
            region, _ = Region.objects.get_or_create(name=region_name)
            regions.append(region)
            for city_name in city_list:
                city, _ = City.objects.get_or_create(region=region, name=city_name)
                cities.append(city)

        self.stdout.write(self.style.SUCCESS(f"Regions: {len(regions)}, Cities: {len(cities)}"))

        makes_data = {
            "Toyota": ["Camry", "Corolla"],
            "BMW": ["5 Series", "3 Series"],
            "Mercedes-Benz": ["E-Class", "C-Class"],
            "Hyundai": ["Elantra", "Sonata"],
            "LADA": ["Vesta", "Granta"],
        }

        makes = []
        car_models = []
        generations = []

        for make_name, model_names in makes_data.items():
            make = Make.objects.get_or_create(name=make_name)[0]
            makes.append(make)
            for model_name in model_names:
                model = CarModel.objects.get_or_create(make=make, name=model_name)[0]
                car_models.append(model)

                for g in ["Gen1", "Gen2", "Gen3"]:
                    gen = Generation.objects.get_or_create(car_model=model, name=g)[0]
                    generations.append(gen)

        body_types = [BodyType.objects.get_or_create(name=n)[0] for n in ["Sedan", "Hatchback", "SUV"]]
        fuel_types = [FuelType.objects.get_or_create(name=n)[0] for n in ["Petrol", "Diesel", "Hybrid"]]
        transmissions = [Transmission.objects.get_or_create(name=n)[0] for n in ["AT", "MT", "CVT"]]
        drive_types = [DriveType.objects.get_or_create(name=n)[0] for n in ["FWD", "RWD", "AWD"]]
        colors = [Color.objects.get_or_create(name=n)[0] for n in ["White", "Black", "Silver", "Blue", "Red"]]
        features = [Feature.objects.get_or_create(name=n)[0] for n in ["AC", "Heated seats", "Rear camera", "Cruise control", "Bluetooth"]]

        self.stdout.write(self.style.SUCCESS("Catalog data created."))

        listings = []

        for i in range(50):
            model = random.choice(car_models)
            gen = random.choice(generations)

            listing = Listing.objects.create(
                user=random.choice(users),
                city=random.choice(cities),

                make=model.make,
                car_model=model,
                generation=gen,

                year=random.randint(2000, 2023),
                mileage_km=random.randint(15_000, 350_000),

                body_type=random.choice(body_types),
                fuel_type=random.choice(fuel_types),
                transmission=random.choice(transmissions),
                drive_type=random.choice(drive_types),
                color=random.choice(colors),

                engine_volume_l=random.choice([1.6, 1.8, 2.0, 2.5, 3.0]),
                power_hp=random.randint(90, 350),

                steering_wheel=random.choice(["left", "right"]),
                condition=random.choice(["new", "used"]),

                vin=f"VINCODE{i:05d}",
                description="Demo listing data",

                price_kzt=random.randint(2_000_000, 30_000_000),
                status=random.choice([ListingStatus.DRAFT, ListingStatus.PUBLISHED]),

                contact_name=f"Seller {i}",
                contact_phone=f"8707{random.randint(1000000, 9999999)}",
            )

            listing.features.add(*random.sample(features, k=random.randint(1, len(features))))

            listings.append(listing)

        self.stdout.write(self.style.SUCCESS(f"Listings created: {len(listings)}"))
        self.stdout.write(self.style.SUCCESS("Demo data SEEDING COMPLETED!"))
