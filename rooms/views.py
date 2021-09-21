from math import ceil
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()

    # (obj, perpage), 10은 per_page 페이지당 보여줄 개수
    paginator = Paginator(room_list, 10)  
    rooms = paginator.get_page(page)

    return render(request, "rooms/home.html", {"rooms": rooms})
