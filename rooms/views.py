from math import ceil
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()

    # (obj, perpage), 10은 per_page 페이지당 보여줄 개수
    # orphans : 마지막 페이지에 보여줄 개수 상한 지정.
    # 예로
    # 1. 마지막 페이지 20페이지가 방개수 5개 이하면
    #    19페이지로 그 5개의 방이 넘어가면서 19페이지에 15개의 방 보임
    # 2. 마지막 페이지가 5개 초과할 경우
    #    마지막 페이지에는 6개부터 방을 보여줌.
    paginator = Paginator(room_list, 10, orphans=5)
    rooms = paginator.page(int(page))
    return render(request, "rooms/home.html", {"page": rooms})
