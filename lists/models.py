from django.db import models
from core import models as core_models


class List(core_models.TimeStampedModel):

    """List Model Definition"""

    name = models.CharField(max_length=80)
    user = models.OneToOneField(
        "users.User", related_name="list", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Order(models.Model):

    list = models.ForeignKey(
        "lists.List", related_name="orders", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="orders", on_delete=models.CASCADE
    )

    number = models.PositiveIntegerField()

    def room_created(self):
        return self.room.created

    def list_user(self):
        return self.list.user

    def count_rooms(self):
        return self.room.count()

    def __str__(self):
        return f"{self.number} {self.room}"
