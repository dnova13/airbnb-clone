from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.shortcuts import render
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


# 장고에 내장된 DetailView 상속
class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room


def search(request):

    # 검색 폼에서 검색한 city 변수의 데이터를 가져옴.
    city = request.GET.get("city")

    # capitalize 앞문자만 대문자로 만들고 나머지 소문자로.
    city = str.capitalize(city)
    return render(request, "rooms/search.html", {"city": city})
