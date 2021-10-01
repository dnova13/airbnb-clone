from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    def get(self, request):

        # 테스트를 위해 initial 로그인 아디 넣음
        form = forms.LoginForm()

        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)

        return render(request, "users/login.html", {"form": form})
