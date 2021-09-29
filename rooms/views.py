from django.views.generic import ListView
from django.urls import reverse
from django.http import Http404
from django.shortcuts import render
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
        # error 는 return 이 아닌 raise 로 그러므로 404 응답 에러는 raise로 반환
        raise Http404()
