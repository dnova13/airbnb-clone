from rest_framework import serializers
from users.serializers import UserSerializer
from rooms.serializers import RelatedRoomsSerializer

from .models import Reservation

# serializers : model -> json , json -> model 로 간편하게 전환하게해줌.


class ReservationListSerializer(serializers.ModelSerializer):

    #  id = serializers.Field()
    id = serializers.ReadOnlyField()
    guest = UserSerializer(read_only=True)
    room = RelatedRoomsSerializer(read_only=True)

    class Meta:
        model = Reservation

        fields = (
            "id",
            "status",
            "room",
            "guest",
            "check_in",
            "check_out",
            "created",
            "updated",
        )
