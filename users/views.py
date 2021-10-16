import os
import requests
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
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
    scope = "read:user user:email"  # 메일 정보를 추출하기위해 스코프 범위 변경.
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )


# 깃 에러에 대한 예외처리 클래스
class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)

        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )

            token_json = token_request.json()

            # 액새스 토큰 가져오는 json 에서 error 키를 가져옴
            # 아무것도 없을시 None으로 기본값 지정.
            error = token_json.get("error", None)

            # 에러가 잇을 경우 에러 발생.
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                # 액세스 토큰 추출하여 유저 정보 가져옴.
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )

                # 이메일 데이터 추출
                email_request = requests.get(
                    "https://api.github.com/user/emails",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )

                email_json = email_request.json()
                profile_json = profile_request.json()

                for obj in email_json:
                    if obj.get("primary") is True and obj.get("verified") is True:
                        email = obj.get("email")

                if email is None:
                    raise GithubException("Can't get access email")

                # 추출한 user 정보에서 login=ID 정보가 잇는지 확인
                username = profile_json.get("login", None)

                # ID 가 잇다면 db 저장 작업 시작
                if username is not None:
                    name = (
                        profile_json.get("name")
                        if profile_json.get("name") is not None
                        else "noname"
                    )
                    email = email
                    bio = (
                        profile_json.get("bio")
                        if profile_json.get("bio") is not None
                        else ""
                    )
                    profile_image = profile_json.get("avatar_url")

                    try:
                        # 해당 메일로 유저 정보가 잇는지 검색.
                        user = models.User.objects.get(username=email)

                        # 로깅 방법 검사.
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )

                    # 유저 정보가 없다면 회원가입 진행.
                    except models.User.DoesNotExist:

                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        # 암호 등록 필요업음을 알림
                        user.set_unusable_password()
                        user.save()

                        if profile_image is not None:
                            photo_request = requests.get(profile_image)
                            user.avatar.save(
                                f"{email}-avatar", ContentFile(photo_request.content)
                            )

                    # 회원 가입 후 로깅 상태로 만듬.
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        # send error message
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)

        if error is not None:
            raise KakaoException("Can't get authorization code.")

        access_token = token_json.get("access_token")

        # 카카오에서 유저 정보 들고옴.
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()

        email = profile_json.get("kakao_account").get("email")

        if email is None:
            raise KakaoException("Please also give me your email")

        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = (
            profile_json.get("kakao_account").get("profile").get("profile_image_url")
        )

        try:
            user = models.User.objects.get(email=email)

            if user.login_method != models.User.LOGING_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")

        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGING_KAKAO,
                email_verified=True,
            )
            # 암호 등록 필요업음을 알림
            user.set_unusable_password()
            user.save()

            if profile_image is not None:
                # 파일 url 을 통해 파일 정보 가져옴.
                photo_request = requests.get(profile_image)

                # photo_request.content : 파일의 이진 정보를 가져옴.
                # ContentFile 을 통해 파일을 담고 저장.
                user.avatar.save(f"{email}-avatar", ContentFile(photo_request.content))

        messages.success(request, f"Welcome back {user.first_name}")
        login(request, user)

        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
