from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Reservation

# serializers : model -> json , json -> model 로 간편하게 전환하게해줌.


class ReviewListSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "status",
            "room",
            "guest",
            "check_in",
            "check_out",
            "created",
            "updated",
        )
