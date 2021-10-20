from django import forms
from django_countries.fields import CountryField
from core.forms import CustomClearableFileInput
from . import models


class SearchForm(forms.Form):

    # initial : 초기값 Anywhere 로 지정
    city = forms.CharField(initial="Anywhere")

    # default : 초기 체크박스 선태값 지정.
    country = CountryField(default="KR").formfield()

    # 방타입을 불러와 셀렉박스 셋팅해줌.
    # 빈칸 --- 보이는게 싫으므로 empty_label을 통해 초기 선택할 텍스트 표시 가능.
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.RoomType.objects.all()
    )

    # required=False : input 박스에서의 required 해제
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)

    # 다선택 체크 박스를 적용하기 위해 아래같이 widget 변겅.
    # widget=forms.CheckboxSelectMultiple
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)

        # pk roomd_id 검색
        room = models.Room.objects.get(pk=pk)

        # photo db 에 룸 삽입
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        )

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room
