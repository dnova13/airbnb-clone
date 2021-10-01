from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            # 장고에서 username은 id 이고
            # 여기서 id는 email로 입력받게함.
            # user 테이블에서 같은 이메일이 있는지 검색
            models.User.objects.get(username=email)
            return email

        # 만약 입력한 이메일 값이 없다면.
        # DoesNotExist 에러 발생
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        return "lalalalalalal"
