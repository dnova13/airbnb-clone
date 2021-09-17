from django.db import models
from core import models as core_models


# 커뮤니케이션 모델(카톡 단톡 방 같은거)
class Conversation(core_models.TimeStampedModel):

    """Conversation Model Definition"""

    # 단체방이니까 참가자들 적으면 됨. 그러므로 n:n
    participants = models.ManyToManyField(
        "users.User", related_name="converstation", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)

        # join을 이용해 배열에 , 붙이며 스트링화
        # "a, b" 로 출력됨
        return ", ".join(usernames)

    # 메세지 수
    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "Number of Messages"

    # 참가자 수
    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"


# 메세지(채팅) 모델, 코어 상속.
class Message(core_models.TimeStampedModel):

    """Message Model Definition"""

    message = models.TextField()

    # 채팅하는 유저
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )

    # 단톡 방.
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
