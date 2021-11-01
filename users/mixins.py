from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


# 메일로 로그인한 경우만 허용할 수 있는 뷰
class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there"))
        return redirect("core:home")


# 오직 로그아웃한(로그인 안한) 사람만이 볼 수 있는 뷰
class LoggedOutOnlyView(UserPassesTestMixin):

    # permission_denied_message = "Page not found"

    def test_func(self):
        # true 값은 유저 인증이 되지 않은경우 : 익명 유저만 통과
        return not self.request.user.is_authenticated

    # test_func false 로 리턴될 경우 허가하지 않게 메소드 코딩
    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there"))
        return redirect("core:home")


# LoginRequiredMixin 상속하여
# 로깅 인증이 안된 유저는 /login 페이지에 보냄
class LoggedInOnlyView(LoginRequiredMixin):

    login_url = reverse_lazy("users:login")
