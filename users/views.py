import os
import requests

# from django import forms
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    # 응답받을 templates html 지정.
    template_name = "users/login.html"

    # 어떤 용도로 쓸지 클래스 지정.
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")

        # next_arg 가 있다면 next에 잇는 url로 반환
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


class SignUpView(mixins.LoggedOutOnlyView, FormView):

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


# 여기서 인자는 url.py 에서 셋팅한 verify/<str:key>
# key 값을로.
# <str:secret> 인 경우 secret 로 변경
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

        # 로그인 성공 메세지 보냄
        messages.success(request, f"Welcome back {user.first_name}")
        login(request, user)

        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.User

    # 연결시킬 html 지정.
    template_name = "users/update-profile.html"

    # 보여줄 폼 필드 설정.
    fields = (
        "first_name",
        "last_name",
        # "username",
        "email",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    success_message = "Profile Updated"

    # 수정하기 위한 객체를 반환함.
    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        # form.fields["avatar"].widget = forms.forms.FileInput()

        # print(form["avatar"])
        # print(vars(form["avatar"]))
        # print(vars(form.fields["avatar"].widget))

        form.fields["birthdate"].label = "Birth date"
        form.fields["birthdate"].widget = forms.forms.DateInput(
            attrs={"type": "date", "label": "Birth date"},
            format="%Y-%m-%d",
        )
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["email"].widget.attrs = {"placeholder": "Email"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bid"}
        form.fields["gender"].widget.choices[0] = ("", "Select Gender")
        form.fields["language"].widget.choices[0] = ("", "Select Language")
        form.fields["currency"].widget.choices[0] = ("", "Select Currency")

        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


def log_out(request):
    messages.info(request, f"See you later")
    logout(request)
    return redirect(reverse("core:home"))
