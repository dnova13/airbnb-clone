from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """Review Admin Definition"""

    # model 에서의 __str__ , rating_average 메소드 호출
    list_display = ("__str__", "rating_average")
