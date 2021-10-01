from django.urls import path
from . import views

app_name = "rooms"

# as_view() 로 RoomDetail view 로 전환
urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]
