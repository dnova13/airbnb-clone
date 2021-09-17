from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "used_by")

    # 이 타입에서 사용되는 방의 개수를 알려줌.
    def used_by(self, obj):
        return obj.rooms.count()

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    fieldsets = (
        (
            "Basic Info",  # 제목
            {"fields": ("name", "description", "country", "address", "price")},  # 목록
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
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

    # 정렬
    ordering = ("name", "price", "bedrooms")

    search_fields = ("=city", "^host__username")

    # horizon 패널은 다대다 관계만 가능.
    filter_horizontal = ("amenities", "facilities", "house_rules")

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

    """ """

    pass
