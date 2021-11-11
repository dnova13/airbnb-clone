import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User



class Command(BaseCommand):

    help = "This command creates users"

    def add_arguments(self, parser):

        # number 입력 없을시 기본은 number = 2, type int로 지정.
        parser.add_argument(
            "--number", default=2, type=int, help="How many users you want to create"
        )
        
        parser.add_argument(
            "--avatar", default=None, type=str, help="Do you add avatar"
        )

    def handle(self, *args, **options):
        number = options.get("number")  # 입력이 없을 경우 2로 받음. = options.get("number", 2)
        ava = options.get("avatar")
        
        seeder = Seed.seeder()
        
        if ava:
            items = {"is_staff": False, "is_superuser": False, "avatar": lambda x: f"avatars/{random.randint(1, 5)}.jpg"}
        
        else:
            items = {"is_staff": False, "is_superuser": False, "avatar": None}
    
        seeder.add_entity(User, number, items)
        seeder.execute()    

        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
