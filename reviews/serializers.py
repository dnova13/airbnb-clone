from rest_framework import serializers
from .models import Review

# serializers : model -> json , json -> model 로 간편하게 전환하게해줌.


class ReviewTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # 사용할 모델 필드 지정.
        fields = ("review", "room", "user")


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("review", "room", "user", "created", "updated")
