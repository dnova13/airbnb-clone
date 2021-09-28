from django.urls import path
from rooms import views as room_views

app_name = "core"

# 홈에서의 기본 url 리스트 작성
# 이제 아까 햇던 all_rooms 함수가 아닌
# HomeView 라는 listview 클래스를 가지고 list view예는
# as_view() 라는 view로 변환시켜주는 메소드를 가지고 잇음.
urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]
