from django.core.validators import ProhibitNullCharactersValidator
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
        return f", ".join(usernames)

    # 메세지 수
    def count_messages(self):
        return self.messages.count()

    def is_over_messges(self):

        msgs = Message.objects.filter(conversation=self)

        is_over_messges = msgs.count() > 150

        if is_over_messges:
            msg_ids = msgs[: msgs.count() - 150].values_list("id", flat=True)
            Message.objects.filter(id__in=msg_ids).delete()

        return is_over_messges

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

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.conversation.pk} {self.user} says: {self.message}"
