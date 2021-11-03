from django.shortcuts import redirect, reverse, render
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from rooms import models as room_models
from . import models
from users import mixins
from django.http import JsonResponse
from django.core.paginator import Paginator

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

        qs = request.user.list.rooms.all()

        page_size = 12
        per_page_cnt = 4

        paginator = Paginator(qs, page_size, orphans=5)
        page = self.request.GET.get("page", 1)
        rooms = paginator.get_page(page)

        start_page = (
            0
            if rooms.number - 2 <= 0
            else rooms.number - 2
            if paginator.num_pages - (rooms.number - 2) > per_page_cnt
            else paginator.num_pages - per_page_cnt
            if paginator.num_pages != per_page_cnt
            else paginator.num_pages - per_page_cnt + 1
        )

        end_page = per_page_cnt + abs(start_page)

        last_range = (
            rooms.number + per_page_cnt - 2
            if paginator.num_pages != per_page_cnt
            else rooms.number + per_page_cnt - 2 + 1
        )

        first_ellipsis = (
            True
            if rooms.number > per_page_cnt - 1
            and paginator.num_pages > per_page_cnt + 1
            else False
        )

        last_ellipsis = (
            True
            if last_range + 1 < paginator.num_pages
            and paginator.num_pages > per_page_cnt + 1
            else False
        )

        # return JsonResponse({"result": True})
        return render(
            request,
            "lists/list_detail.html",
            {
                "rooms": rooms,
                "page_obj": rooms,
                "page_range": paginator.page_range[abs(start_page) : end_page],
                "last_range": last_range,
                "first_ellipsis": first_ellipsis,
                "last_ellipsis": last_ellipsis,
            },
        )
