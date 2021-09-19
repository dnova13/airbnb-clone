from django.core.management.base import BaseCommand
from rooms.models import HouseRule


class Command(BaseCommand):

    help = "This command creates house roule"

    def handle(self, *args, **options):
        rules = ["Pets allowed", "Smoking allowed"]
        for r in rules:
            HouseRule.objects.create(name=r)

        self.stdout.write(self.style.SUCCESS(f"{len(rules)} house roule created!"))
