import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models


class BookedDay(core_models.TimeStampedModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)


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
    is_reviewed = models.BooleanField(default=False)
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

        is_finished = now > self.check_out

        # 사용이 완료 되면 해당 예약의 날짜 데이터 지움.
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()

        return is_finished

    # 화면 표시를 아이콘으로 변경
    is_finished.boolean = True

    def save(self, *args, **kwargs):

        # 예약된게 없으면 예약된 날짜 추가
        if self.pk is None:

            start = self.check_in
            end = self.check_out

            difference = end - start

            # 체크인 체크 아웃 날짜범위에 예약된게 있는지 찾아서 true 반환.
            existing_booked_day = BookedDay.objects.filter(
                reservation__room=self.room, day__range=(start, end)
            ).exists()

            # 예약이 없다면 예약정보와 예약 날짜들 저장
            if not existing_booked_day:

                # resevation 저장하여 포린키 형성
                super().save(*args, **kwargs)

                # 예약된 날짜 담음.
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return

        # 예약된게 있다면 그냥 save(수정)
        else:
            return super().save(*args, **kwargs)
