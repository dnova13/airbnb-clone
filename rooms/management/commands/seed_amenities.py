from django.core.management.base import BaseCommand
from rooms.models import Amenity  # Amenity 임포트


class Command(BaseCommand):

    help = "This command tells me that he loves me"

    """ def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell you that I love you?"
        )
        """

    def handle(self, *args, **options):
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]

        #  amenities 배열을 통해 관련 내용을 등록
        for amenity in amenities:
            Amenity.objects.create(name=amenity)  # name = a
        self.stdout.write(self.style.SUCCESS("Amenities created!"))
