from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rooms import models as room_models
from . import models
from users import mixins


# 선호하는 방 추가
@login_required
def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)

    if room is not None and action is not None:

        # get_or_create : 해당 데이터가 있으면 get, 없으면 데이터 생성함.
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name="My Favourites Houses"
        )
        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)

    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(mixins.LoggedInOnlyView, TemplateView):

    template_name = "lists/list_detail.html"
