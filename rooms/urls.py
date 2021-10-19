from django.urls import path
from . import views

app_name = "rooms"

# as_view() 로 RoomDetail view 로 전환
urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.EditRoomView.as_view(), name="photos"),
    path("search/", views.SearchView.as_view(), name="search"),
]
