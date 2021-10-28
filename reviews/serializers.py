from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Review

# serializers : model -> json , json -> model 로 간편하게 전환하게해줌.


class ReviewTestSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer()

    class Meta:
        model = Review
        # 사용할 모델 필드 지정.
        fields = ("review", "room", "user")


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


""" 
    review 
    accuracy 
    communication
    cleanliness 
    location 
    check_in
    value 
    user 
    room  """
