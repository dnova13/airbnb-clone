from django.urls import path
from . import views
from django.views.i18n import JavaScriptCatalog
from django.conf.urls.i18n import i18n_patterns

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
    path("list/<str:noun>/", views.list_reservations, name="api_list"),
]

# urlpatterns = i18n_patterns(urlpatterns)
