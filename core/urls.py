from django.urls import path
from rooms import views as room_views

app_name = "core"

# 홈에서의 기본 url 리스트 작성
urlpatterns = [path("", room_views.all_rooms, name="home")]
