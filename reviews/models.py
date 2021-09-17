from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()

    #
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()

    # 사용자에 종속되므로 포린키 사용
    # string으로 객체 적을 때 주의사황
    # 이전거는 이 코드 위에 User 임포트해서 'User'라고 적었지만
    # 이번에는 임포트 없이 장고에서 자동처리하기 위헤서
    # "폴더명.클래스" 명 꼭 적어 져야됨. users.User 이렇게
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )

    # 룸에 종속되므로 포린키 사용
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.room}"

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    # 닉네임 지정.
    rating_average.short_description = "Avg."
