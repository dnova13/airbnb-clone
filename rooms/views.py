from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.shortcuts import render
from django_countries import countries  # 나라 항목 임포트
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
    # get에 아무데이터가 없는 None 일때
    # 디폴트 값 'Anywhere'  로 지정
    city = request.GET.get("city", "Anywhere")
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))

    # capitalize 앞문자만 대문자로 만들고 나머지 소문자로.
    city = str.capitalize(city)

    # db 에서 룸타입 다 가져옴.
    room_types = models.RoomType.objects.all()

    # 서치 폼에서 검색한 조건들.
    form = {
        "city": city,
        "s_room_type": room_type,  # 선택한 룸 타입
        "s_country": country,  # 선택한 나라
    }

    # 각 검색 태그에 들어갈 선택 조건들
    choices = {
        "countries": countries,
        "room_types": room_types,
    }

    return render(request, "rooms/search.html", {**form, **choices})
