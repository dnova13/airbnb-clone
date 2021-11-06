from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Message

# serializers : model -> json , json -> model 로 간편하게 전환하게해줌.


class MessagesSerializer(serializers.ModelSerializer):

    #  id = serializers.Field()
    id = serializers.ReadOnlyField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message

        fields = (
            "id",
            "user",
            "message",
            "conversation",
            "is_read",
            "created",
            "updated",
        )
