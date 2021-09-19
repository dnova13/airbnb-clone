from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "used_by")

    # 이 타입에서 사용되는 방의 개수를 알려줌.
    def used_by(self, obj):
        return obj.rooms.count()

    pass


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                    "room_type",
                )
            },
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {"fields": ("amenities", "facilities", "house_rules")},
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",  # 소모품 카운트 함수 추가
        "count_photos",  # 사진 수 함수 추가
        "total_rating",
    )

    # 포린키 호스트에서 다른거 보여주고 싶다면
    # host__superhost  이렇게 적으면됨
    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)

    # 정렬
    ordering = ("name", "price", "bedrooms")

    search_fields = ("=city", "^host__username")

    # horizon 패널은 다대다 관계만 가능.
    filter_horizontal = ("amenities", "facilities", "house_rules")

    """ def save_model(self, request, obj, form, change):
        print(obj, change, form)
        super().save_model(request, obj, form, change) """

    # 함수 추가
    # self 는 여기 room class 고
    # model의 row 값임. 자세한거 문서 참조
    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    # count_amenities.short_description = "ffff"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Phot Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # mark_safe : 이 안에 쓴 input 내용들은 안전하니 쓰라고 알려줌.
        return mark_safe(f'<img width="250px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
