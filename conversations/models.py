from django.db import models
from core import models as core_models


# 커뮤니케이션 모델(카톡 단톡 방 같은거)
class Conversation(core_models.TimeStampedModel):

    """Conversation Model Definition"""

    # 단체방이니까 참가자들 적으면 됨. 그러므로 n:n
    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        # self.created 그냥 쓰면 에러가 나므로 string화 해줘야됨.
        return str(self.created)


# 메세지(채팅) 모델, 코어 상속.
class Message(core_models.TimeStampedModel):

    """Message Model Definition"""

    message = models.TextField()

    # 채팅하는 유저
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    # 단톡 방.
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} says: {self.message}"
