import os
import requests
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):

    # 응답받을 templates html 지정.
    template_name = "users/login.html"

    # 어떤 용도로 쓸지 클래스 지정.
    form_class = forms.LoginForm

    # 해당 요청 예로 로그인 성공시 리다렉 지정.
    # reverse를 통해 ("core:home") 이 적용 안됨
    # reverse_lazy 이용
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    # 초기값 지정 일단 예로 보여준거고 실제 회원가입 폼에서 쓸필요가 없음.
    # initial = {"first_name": "Nicoas", "last_name": "Serr", "email": "itn@las.com}

    def form_valid(self, form):

        # form 이 유효하면 form save 함.
        form.save()

        # 회원 가입 후 바로 로그인하기 위한 과정을 위해 아래 작성.
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        user.verify_email()

        return super().form_valid(form)


# 여기서 인자 key 해도 되고, secrect 해도 상관없은 내키는대로
def complete_verification(request, key):

    try:
        # 메일 인증하면서 보낸 시크릿 키 검사
        user = models.User.objects.get(email_secret=key)

        # 유효성 통과시 db 저장하고 , 시크릿 키 초기화
        user.email_verified = True
        user.email_secret = ""
        user.save()

        # 메세지 동작은 추후 나중에
        # to do: add succes message
    except models.User.DoesNotExist:
        # to do: add error message
        pass

    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


def github_callback(request):
    client_id = os.environ.get("GH_ID")
    client_secret = os.environ.get("GH_SECRET")
    code = request.GET.get("code", None)

    if code is not None:
        request = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )
        print(request.json())
    else:
        return redirect(reverse("core:home"))


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
