from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin


# 오직 로그아웃한(로그인 안한) 사람만이 볼 수 있는 뷰
class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page not found"

    def test_func(self):
        # true 값은 유저 인증이 되지 않은경우 : 익명 유저만 통과
        return not self.request.user.is_authenticated

    # test_func false 로 리턴될 경우 허가하지 않게 메소드 코딩
    def handle_no_permission(self):
        return redirect("core:home")
