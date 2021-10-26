from django.db import models
from django.utils import timezone
from core import models as core_models


class BookedDay(core_models.TimeStampedModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"


class Reservation(core_models.TimeStampedModel):

    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    # 셀렉트 박스 작성.
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    # 사용중 표시
    # 체크인한 시간과 체크 아웃 시간 내에 잇으면 사용중.
    def in_progress(self):
        now = timezone.now().date()
        # return False
        return now >= self.check_in and now <= self.check_out

    # 화면 표시를 아이콘으로 변경
    in_progress.boolean = True

    # 방 사용 완료 끝난거 표시
    def is_finished(self):
        now = timezone.now().date()
        print(now)
        # return False
        return now > self.check_out

    # 화면 표시를 아이콘으로 변경
    is_finished.boolean = True

    def save(self, *args, **kwargs):

        # 예약된게 없으면 예약된 날짜 추가
        if self.pk is None:
            print("new")
            start = self.check_in
            end = self.check_out

            diff = end - start

            # 체크인 체크 아웃 날짜범위에 예약된게 있는지 찾아서 true 반환.
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end)
            ).exists()

        # 예약된게 있다면 그냥 save
        else:
            return super().save(*args, **kwargs)
