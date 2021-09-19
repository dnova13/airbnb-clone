import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


NAME = "lists"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        # 리스트에서 포린키 사용자 정보만 수정 후 삽입
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users)}
        )

        created = seeder.execute()

        # 삽입한 리스트 pk value 배열화
        cleaned = flatten(list(created.values()))

        for pk in cleaned:
            # pk 와 일치한 리스트 가져옴.
            list_model = list_models.List.objects.get(pk=pk)

            # rooms 배열에서 시작 0-5 와 끝 6-30 범위 랜덤으로 배열 가져옴.
            # ex) roomm [1 : 15] : 1-15 까지의 배열 가져옴.
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]

            # '*to_add' 를 붙어서 list_model 배열의 요소들을 뒤에 덫붙임
            # add(to_add) 를 하지 않는 이유는 서로 타입이 안 맞기 때문에
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
