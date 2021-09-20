from django.shortcuts import render
from . import models


def all_rooms(request):
    # page 키로 값을 받고, 아무것도 받지않는다면 디폴트로 1을 설정
    page = int(request.GET.get("page", 1))  # int 로 변화
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]

    return render(request, "rooms/home.html", {"rooms": all_rooms})
