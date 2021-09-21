from math import ceil
from django.shortcuts import render
from . import models


def all_rooms(request):
    # page 키로 값을 받고, 아무것도 받지않는다면 디폴트로 1을 설정
    page = int(request.GET.get("page", 1))  # int 로 변화
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)

    return render(
        request,
        "rooms/home.html",
        {
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count),
        },
    )
