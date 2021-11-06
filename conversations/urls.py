from django.urls import path
from . import views

app_name = "conversations"

urlpatterns = [
    path("go/<int:a_pk>/<int:b_pk>", views.go_conversation, name="go"),
    path("list/", views.ConversationListView.as_view(), name="list"),
    path("<int:pk>/", views.ConversationDetailView.as_view(), name="detail"),
    path("<int:pk>/send/", views.create_msg, name="send"),
    path("<int:pk>/read/", views.read_msg, name="read"),
]
