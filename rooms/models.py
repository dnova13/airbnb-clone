from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 하나의 방에서는
# 방 타입뿐만 아니라
# 방에서 제공하는 소모품(Amenity), 시설(Facility) 등이 잇으므로
# 이 방 모델 클래스에 하위에 속하는 자식 클래스들을 적음.
# 이 자식 클라스에 각각의 아이템들은 AbstractItem 으로 확장받아 고드 중복을 없앤다.
# 예로 이름 무조건 필요하니
# `name = models.CharField(max_length=80)` 이런 중복된 코드 적는걸 막는다.
class RoomType(AbstractItem):

    """RoomType Model Definition"""

    pass


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    pass


class Facility(AbstractItem):

    """Facility Model Definition"""

    pass


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    pass


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity)
    facilities = models.ManyToManyField(Facility)
    house_rules = models.ManyToManyField(HouseRule)

    def __str__(self):
        return self.name
