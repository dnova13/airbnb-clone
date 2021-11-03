from django.shortcuts import redirect, reverse, render
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from rooms import models as room_models
from . import models
from users import mixins
from django.http import JsonResponse

# 선호하는 방 추가
@login_required
def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)

    if room is not None and action is not None:

        # get_or_create : 해당 데이터가 있으면 get, 없으면 데이터 생성함.
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name="My Favorite Houses"
        )
        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)

    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(mixins.LoggedInOnlyView, TemplateView):

    template_name = "lists/list_detail.html"

    def get(self, request, *args, **kwargs):

        # request.GET.ge

        page_size = 12

        # qs = models.List.objects.get(user=request.user, name="My Favorite Houses")

        # print(qs.rooms.all().values())

        page = request.GET.get("page", 1)

        # return JsonResponse({"result": True})
        return render(
            request,
            "lists/list_detail.html",
            {
                "rm": "qs",
            },
        )
