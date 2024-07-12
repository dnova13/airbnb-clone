import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from django.conf.urls.i18n import i18n_patterns
from utills.utill import get_cls_attr

try:
    import local_settings
except ImportError:
    import test_settings as local_settings

def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("users/", include("users.urls", namespace="users")),
    path("reservations/", include("reservations.urls", namespace="reservations")),
    path("reviews/", include("reviews.urls", namespace="reviews")),
    path("lists/", include("lists.urls", namespace="lists")),
    path("conversations/", include("conversations.urls", namespace="conversations")),
    path(get_cls_attr(local_settings, 'DJANGO_ADMIN', 'admin/'), admin.site.urls),

    path("api/v1/reviews/", include("reviews.urls", namespace="reviews_api")),
    path("api/v1/reservations/",
         include("reservations.urls", namespace="reservations_api")),
    path("api/v1/conversations/",
         include("conversations.urls", namespace="conversations_api")),

    path("sentry-debug/", trigger_error),
]

urlpatterns += i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
)

# debug 모드 일 경우
if local_settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)