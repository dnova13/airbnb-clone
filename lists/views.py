from django.shortcuts import redirect, reverse
from rooms import models as room_models
from . import models


# 선호하는 방 추가
def save_room(request, room_pk):
    room = room_models.Room.objects.get_or_none(pk=room_pk)

    if room is not None:
        # get_or_create : 해당 데이터가 있으면 get, 없으면 데이터 생성함.
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name="My Favourites Houses"
        )
        the_list.rooms.add(room)

    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
