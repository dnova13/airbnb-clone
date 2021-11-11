from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.utils import timezone
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users import mixins as user_mixins
from django.contrib.messages.views import SuccessMessageMixin
from core.forms import CustomClearableFileInput
from . import models, forms


# 장고에 내장된 list view 상속
class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room

    # 페이지에서 보일 목록의 개수
    paginate_by = 12
    paginate_orphans = 0

    # 정렬 : 내림차순, 오름차순 "created"
    ordering = "-created"

    # page_range = self.paginator.get_elided_page_range(number=10)

    # object 이름을 rooms 로 변경
    context_object_name = "rooms"

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # 장고 ListView 에서 paginator 속성 얻어오는 과정.
        queryset = object_list if object_list is not None else self.object_list
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )

        per_page_cnt = 4

        start_page = (
            0
            if page.number - 2 <= 0
            else page.number - 2
            if paginator.num_pages - (page.number - 2) > per_page_cnt
            else paginator.num_pages - per_page_cnt
            if paginator.num_pages != per_page_cnt
            else paginator.num_pages - per_page_cnt + 1
        )

        end_page = per_page_cnt + abs(start_page)

        last_range = (
            page.number + per_page_cnt - 2
            if paginator.num_pages != per_page_cnt
            else page.number + per_page_cnt - 2 + 1
        )

        first_ellipsis = (
            True
            if page.number > per_page_cnt - 1 and paginator.num_pages > per_page_cnt + 1
            else False
        )

        last_ellipsis = (
            True
            if last_range + 1 < paginator.num_pages
            and paginator.num_pages > per_page_cnt + 1
            else False
        )

        now = timezone.now()
        context["now"] = now
        context["page_range"] = paginator.page_range[abs(start_page) : end_page]
        context["last_range"] = last_range
        context["first_ellipsis"] = first_ellipsis
        context["last_ellipsis"] = last_ellipsis

        return context


# 장고에 내장된 DetailView 상속
class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room


# 장고에 내장된 View 상송
class SearchView(View):

    """SearchView Definition"""

    def get(self, request):

        if not request.GET.get("country"):
            _req = request.GET.copy()
            _req.__setitem__("country", "KR")
            form = forms.SearchForm(_req)
        else:
            form = forms.SearchForm(request.GET)

        # form.is_valid : form 에 에러가 잇는지 없느지 감지
        # 에러가 없을 경우 true로 반환
        if form.is_valid():

            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}

            if city:
                filter_args["city__istartswith"] = city

            filter_args["country"] = country

            # != 0 에서 is not None 으로 장고 form 이 값대로 조건 변경.
            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            # 이전에 len(amenities) 길이 체크할 필요없이
            # 이미 유효성 체크 햇으므로 아래와 같이 바로 적을 수 잇음.
            for amenity in amenities:
                filter_args["amenities"] = amenity

            for facility in facilities:
                filter_args["facilities"] = facility

            qs = models.Room.objects.filter(**filter_args).order_by("-created")

            page_size = 12
            per_page_cnt = 4

            paginator = Paginator(qs, page_size, orphans=0)
            page = request.GET.get("page", 1)
            rooms = paginator.get_page(page)

            start_page = (
                0
                if rooms.number - 2 <= 0
                else rooms.number - 2
                if paginator.num_pages - (rooms.number - 2) > per_page_cnt
                else paginator.num_pages - per_page_cnt
                if paginator.num_pages != per_page_cnt
                else paginator.num_pages - per_page_cnt + 1
            )

            end_page = per_page_cnt + abs(start_page)

            last_range = (
                rooms.number + per_page_cnt - 2
                if paginator.num_pages != per_page_cnt
                else rooms.number + per_page_cnt - 2 + 1
            )

            first_ellipsis = (
                True
                if rooms.number > per_page_cnt - 1
                and paginator.num_pages > per_page_cnt + 1
                else False
            )

            last_ellipsis = (
                True
                if last_range + 1 < paginator.num_pages
                and paginator.num_pages > per_page_cnt + 1
                else False
            )

            current_url = "".join(request.get_full_path().split("page")[0])

            if current_url[-1] != "&":
                current_url = "".join(request.get_full_path().split("page")[0]) + "&"

            return render(
                request,
                "rooms/search.html",
                {
                    "form": form,
                    "rooms": rooms,
                    "page_obj": rooms,
                    "current_url": current_url,
                    "page_range": paginator.page_range[abs(start_page) : end_page],
                    "last_range": last_range,
                    "first_ellipsis": first_ellipsis,
                    "last_ellipsis": last_ellipsis,
                },
            )

        return render(request, "rooms/search.html", {"form": form})


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["amenities"].widget = forms.forms.CheckboxSelectMultiple()
        form.fields["amenities"].queryset = form["amenities"].field._queryset

        form.fields["facilities"].widget = forms.forms.CheckboxSelectMultiple()
        form.fields["facilities"].queryset = form["facilities"].field._queryset

        form.fields["house_rules"].widget = forms.forms.CheckboxSelectMultiple()
        form.fields["house_rules"].queryset = form["house_rules"].field._queryset

        form.fields["check_in"].widget = forms.forms.TimeInput(
            format="%H:%M", attrs={"type": "time"}
        )

        form.fields["check_out"].widget = forms.forms.TimeInput(
            format="%H:%M", attrs={"type": "time"}
        )

        form.fields["country"].widget.choices[0] = ("", "Select Country")

        # ModelChoiceField 일경우 빈 라벨 제목 지정  empty field 로
        form.fields["room_type"].empty_label = "Select Room Type"

        return form

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        messages.success(self.request, "Room Uploaded")

        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    # 사용자에 대한 필터 처리
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)

        # 이 룸의 주인이 아니라면 못들어게 함.
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["amenities"].widget = forms.forms.CheckboxSelectMultiple()
        form.fields["amenities"].queryset = form["amenities"].field._queryset

        form.fields["facilities"].widget = forms.forms.CheckboxSelectMultiple()
        form.fields["facilities"].queryset = form["facilities"].field._queryset

        form.fields["house_rules"].widget = forms.forms.CheckboxSelectMultiple()
        form.fields["house_rules"].queryset = form["house_rules"].field._queryset

        form.fields["check_in"].widget = forms.forms.TimeInput(
            format="%H:%M", attrs={"type": "time"}
        )

        form.fields["check_out"].widget = forms.forms.TimeInput(
            format="%H:%M", attrs={"type": "time"}
        )

        form.fields["country"].widget.choices[0] = ("", "Select Country")
        form.fields["room_type"].empty_label = "Select Room Type"

        return form


@login_required  # 로그인일때 만 실행 아니면 셋팅된곳으로 리다렉
def delete_room(request, pk):
    user = request.user

    try:
        room = models.Room.objects.get(pk=pk)

        # 로그인 사용자 인지 확인
        if room.host.pk != user.pk:
            messages.error(request, "Cant delete the room")
        else:
            models.Room.objects.filter(pk=pk).delete()
            messages.success(request, "Photo Deleted")

        return redirect(reverse("core:home"))

    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required  # 로그인일때 만 실행 아니면 셋팅된곳으로 리다렉
def delete_photo(request, room_pk, photo_pk):
    user = request.user

    try:
        room = models.Room.objects.get(pk=room_pk)

        # 로그인 사용자 인지 확인
        if room.host.pk != user.pk:
            messages.error(request, "Cant delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")

        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))

    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"  # photo_pk를 pk 대신 사용.
    success_message = "Photo Updated"
    fields = (
        "caption",
        "file",
    )

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["file"].label = "Image"
        form.fields["file"].widget = CustomClearableFileInput()

        return form

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "rooms/photo_create.html"
    fields = ("caption", "file")
    form_class = forms.CreatePhotoForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["file"].label = "Image"
        form.fields["file"].widget = CustomClearableFileInput()

        return form

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")

        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))
