from django.views.generic import ListView
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from . import models


# 장고에 내장된 list view 상속
class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room

    # 페이지에서 보일 목록의 개수
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"

    # object 이름을 rooms 로 변경
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


def room_detail(request, pk):
    try:
        # db에서 해당 pk 즉 아이디에서의 방정보를 가져옴.
        room = models.Room.objects.get(pk=pk)

        # db 에서 방하나의 정보를 랜더함.
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:

        # 이전 url 장고 기법 활용하여 "/" 로 리다렉
        return redirect(reverse("core:home"))
