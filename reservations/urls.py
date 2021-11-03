from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [
    path(
        "create/<int:room>/<int:year>-<int:month>-<int:day>/<int:timedelta>",
        views.create_reservation,
        name="create",
    ),
    path("list/", views.ReservationListView.as_view(), name="list"),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail"),
    path("<int:pk>/<str:verb>", views.edit_reservation, name="edit"),
    path("api/list/<str:noun>/", views.list_reservations, name="api_list"),
]
