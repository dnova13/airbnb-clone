from io import StringIO
import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
from django.utils import timezone


class Command(BaseCommand):
    
    help = "This command creates rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms you want to create",
        )

        parser.add_argument(
            "--country",
            default="",
            type=str,
            help="How many rooms you want to create",
        )

        parser.add_argument(
            "--city",
            default="",
            type=str,
            help="How many rooms you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        country = options.get("country")
        city = options.get("city")

        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()

        items = {
            "name": lambda x: seeder.faker.address(),
            "host": lambda x: random.choice(all_users),
            "room_type": lambda x: random.choice(room_types),
            "guests": lambda x: random.randint(1, 20),
            "price": lambda x: random.randint(1, 300),
            "beds": lambda x: random.randint(1, 5),
            "bedrooms": lambda x: random.randint(1, 5),
            "baths": lambda x: random.randint(1, 5),
            # "created": lambda x: timezone.now()
        }

        if country:
            items.__setitem__("country", country)

        if city:
            items.__setitem__("city", city)

        seeder.add_entity(
            room_models.Room,
            number,
            items,
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))

        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)

            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 90)}.jpg",
                )
            for a in amenities:
                # 0-15 랜덤으로 숫자생성
                magic_number = random.randint(0, 15)
                # 2로 나눠지면 amenity 를 추가함
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
