from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    """List Admin Definition"""

    list_display = ("name", "user", "count_rooms")

    # 이름으로 검색하는 서치바 생성
    search_fields = ("name",)

    # 다 대 다 필터 생성
    filter_horizontal = ("rooms",)
