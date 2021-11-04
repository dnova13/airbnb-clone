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
        # (<data> , <생성 여부 확인> ) 튜플로 받음
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name="My Favorite Houses"
        )

        orders = models.Order.objects.filter(list=the_list).order_by("-id")

        if not orders and action == "add":
            models.Order.objects.create(room=room, list=the_list, number=1)
        elif orders:
            try:
                _room = orders.get(room=room)
            except Exception:
                _room = None

            if action == "add" and not _room:
                models.Order.objects.create(
                    room=room, list=the_list, number=orders[0].number + 1
                )
            elif action == "remove" and _room:
                _room.delete()

    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(mixins.LoggedInOnlyView, TemplateView):

    template_name = "lists/list_detail.html"

    def get(self, request, *args, **kwargs):

        qs = (
            models.Order.objects.filter(
                list__user=request.user, list__name="My Favorite Houses"
            )
            .order_by("-id")
            .order_by("-room__created")
        )

        page_size = 12
        per_page_cnt = 4

        paginator = Paginator(qs, page_size, orphans=0)
        page = self.request.GET.get("page", 1)
        orders = paginator.get_page(page)

        start_page = (
            0
            if orders.number - 2 <= 0
            else orders.number - 2
            if paginator.num_pages - (orders.number - 2) > per_page_cnt
            else paginator.num_pages - per_page_cnt
            if paginator.num_pages != per_page_cnt
            else paginator.num_pages - per_page_cnt + 1
        )

        end_page = per_page_cnt + abs(start_page)

        last_range = (
            orders.number + per_page_cnt - 2
            if paginator.num_pages != per_page_cnt
            else orders.number + per_page_cnt - 2 + 1
        )

        first_ellipsis = (
            True
            if orders.number > per_page_cnt - 1
            and paginator.num_pages > per_page_cnt + 1
            else False
        )

        last_ellipsis = (
            True
            if last_range + 1 < paginator.num_pages
            and paginator.num_pages > per_page_cnt + 1
            else False
        )

        print(start_page)
        print(end_page)
        print(paginator.page_range[abs(start_page) : end_page])
        print(last_range)

        return render(
            request,
            "lists/list_detail.html",
            {
                "orders": orders,
                "page_obj": orders,
                "page_range": paginator.page_range[abs(start_page) : end_page],
                "last_range": last_range,
                "first_ellipsis": first_ellipsis,
                "last_ellipsis": last_ellipsis,
            },
        )
