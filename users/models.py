import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core import managers as core_managers


def file_size(value):
    MB = 1024 * 1024
    limit = 2 * MB

    if value.size > limit:
        raise ValidationError(_("File too large. Size should not exceed 2 MiB."))
    else:
        return value

class User(AbstractUser):
   
    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, _("English")),
        (LANGUAGE_KOREAN, _("Korean")),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGING_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGING_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True, validators=[file_size])
    gender = models.CharField(
        _("gender"), choices=GENDER_CHOICES, max_length=10, blank=True
    )
    bio = models.TextField(_("bio"), blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        _("language"),
        choices=LANGUAGE_CHOICES,
        max_length=2,
        blank=True,
        default=LANGUAGE_KOREAN,
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)

    # 메일 인증 검증
    email_verified = models.BooleanField(default=False)

    # 메일 인증키
    email_secret = models.CharField(max_length=20, default="", blank=True)

    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    objects = core_managers.CustomUserManager()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    # 메일 인증 메소드
    def verify_email(self):

        # 메일 인증을 안한 경우 (회원 가입을 하는 경우)
        if self.email_verified is False:

            # uuid 사용 20글자 시크릿 출력
            secret = uuid.uuid4().hex[:20]

            # 해당 db 데이터에 eamil_secret 값 삽입
            self.email_secret = secret

            # render_to_string : templte를 로드하여 render 하는거.
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )

            send_mail(
                _("Verify Airbnb Account"),  # 메일 제목
                strip_tags(html_message),  # 메일 메세지, strip_tags : 태그를 제회하고 문자로 반환
                settings.EMAIL_FROM,  # 발신 메일
                [self.email],  # 보낼 메일 주소 리스트
                fail_silently=False,  # 에러 발생시 처리 유무
                html_message=html_message,  # html 메시지
            )

            self.save()
        return
