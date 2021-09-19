from django.core.management.base import BaseCommand
from rooms.models import RoomType


class Command(BaseCommand):

    help = "This command creates room type"

    def handle(self, *args, **options):
        roomType = [
            "Entire place",
            "Private room",
            "Hotel room",
            "Shared room",
        ]
        for rt in roomType:
            RoomType.objects.create(name=rt)

        self.stdout.write(self.style.SUCCESS(f"{len(roomType)} facilities room type!"))
