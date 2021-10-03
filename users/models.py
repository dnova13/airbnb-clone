import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail


class User(AbstractUser):

    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)

    # 메일 인증 검증
    email_verified = models.BooleanField(default=False)

    # 메일 인증키
    email_secret = models.CharField(max_length=20, default="", blank=True)

    # 메일 인증 메소드
    def verify_email(self):

        # 메일 인증을 안한 경우 (회원 가입을 하는 경우)
        if self.email_verified is False:

            # uuid 사용 20글자 시크릿 출력
            secret = uuid.uuid4().hex[:20]

            # 해당 db 데이터에 eamil_secret 값 삽입
            self.email_secret = secret

            send_mail(
                "Verify Airbnb Account",  # 메일 제목
                f"Verify account, this is your secret: {secret}",  # 메일 메세지
                settings.EMAIL_FROM,  # 발신 메일
                [self.email],  # 보낼 메일 주소 리스트
                fail_silently=False,  # 에러 발생시 처리 유무
            )
        return
