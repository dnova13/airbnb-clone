from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    """List Admin Definition"""

    list_display = (
        "name",
        "user",  # "count_rooms"
    )

    # 이름으로 검색하는 서치바 생성
    search_fields = ("name",)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "room",
        "list",
        "list_user",
        "number",
        "room_created",
    )
