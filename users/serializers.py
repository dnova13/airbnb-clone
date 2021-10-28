from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
            "password",
        )

        read_only_fields = ("id", "superhost", "avatar")

    def validate_first_name(self, value):
        return value.upper()
