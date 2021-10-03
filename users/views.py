from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


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

    """ def get(self, request):

        form = forms.LoginForm()

        return render(request, "users/login.html", {"form": form}) """

    """ def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                #
                return redirect(reverse("core:home"))

        return render(request, "users/login.html", {"form": form}) """


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
