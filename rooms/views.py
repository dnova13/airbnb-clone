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
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))  # 즉시 예약 체크
    superhost = bool(request.GET.get("superhost", False))  # 슈퍼 호스트인지 체크
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    # capitalize 앞문자만 대문자로 만들고 나머지 소문자로.
    city = str.capitalize(city)

    # 서치 폼에서 검색한 조건들.
    form = {
        "city": city,
        "s_room_type": room_type,  # 선택한 룸 타입
        "s_country": country,  # 선택한 나라
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    # db 에서 작성한 각 타입들의 가져옴.
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    # 각 검색 태그에 들어갈 선택 조건들
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:  # lte <=
        filter_args["price__lte"] = price

    if guests != 0:  # gte =>
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    # superhost 같은 경우 user 모델에 등록되어 있으므로
    # foreign key 를 이용해 아래와 같이 필터링 가능.
    if superhost is True:
        filter_args["host__superhost"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
