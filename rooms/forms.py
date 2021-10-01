from django import forms
from . import models


class SearchForm(forms.Form):

    # initial : 초기값 Anywhere 로 지정
    city = forms.CharField(initial="Anywhere")

    # required=False : input 박스에서의 required 해제
    price = forms.IntegerField(required=False)

    # 방타입을 불러와 셀렉박스 셋팅해줌.
    room_type = forms.ModelChoiceField(queryset=models.RoomType.objects.all())
