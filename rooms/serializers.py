from rest_framework import serializers
from .models import Room


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

        # read_only_fields = ("id", "superhost", "avatar")

    def validate_first_name(self, value):
        return value.upper()


class RelatedRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "name",
            "country",
            "city",
            "address",
            "created",
            "updated",
            "first_photo",
            "host",
        )

        # read_only_fields = ("id", "superhost", "avatar")

    def validate_first_name(self, value):
        return value.upper()
