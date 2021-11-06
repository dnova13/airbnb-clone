from django.core import validators
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator
from core import models as core_models
from cal import Calendar
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def file_size(value): 
    MB = 1024 * 1024
    limit = 2 * MB

    if value.size > limit:
        raise ValidationError(_("File too large. Size should not exceed 2 MiB."))


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        # 추상 모델 허용.
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Model Definition"""

    pass

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    # 사진에 대한 설명
    caption = models.CharField(max_length=80)

    #  이미지 파일
    file = models.ImageField(upload_to="room_photos", validators=[file_size])

    # 방이 삭제 되면 거기에 종속된 포토도 삭제
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField(validators=[MinValueValidator(1)])
    bedrooms = models.IntegerField(validators=[MinValueValidator(1)])
    baths = models.IntegerField(validators=[MinValueValidator(1)])
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    # __str__ 처럼 sava() 오버라이딩, 자세한거는 문서 참조
    # https://docs.djangoproject.com/en/3.2/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    # 방 총점 구함.
    def total_rating(self):
        all_reviews = self.reviews.all()  # 쿼리셋 이용하여 룸에 잇는 리뷰 다 불러옴.
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()

        # 삼항 연산자로 review가 하나도 없을때는 계산 안하고 0으로
        return round(all_ratings / len(all_reviews), 2) if len(all_reviews) > 0 else 0

    # 첫번째 사진 url 를 보냄.
    def first_photo(self):

        try:
            # unpacking value,  배열에서 첫번째 것를 담음
            # 다른 예로 배열이 2개일 때, 이렇게 담는거 가능 one, two = self.photos.all()[:2]
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()

        this_year = now.year
        this_month = now.month

        next_month = (this_month + 1) % 12 if (this_month + 1) % 12 != 0 else 12
        next_year = this_year if this_month < next_month else this_year + 1
        next2_month = (this_month + 2) % 12 if (this_month + 2) % 12 != 0 else 12
        next2_year = this_year if this_month < next2_month else this_year + 1

        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(next_year, next_month)
        next2_month_cal = Calendar(next2_year, next2_month)

        return [this_month_cal, next_month_cal, next2_month_cal]
