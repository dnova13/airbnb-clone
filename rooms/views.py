from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage  # EmptyPage 예외 사항 적용하기 위해 임포트
from . import models


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")
