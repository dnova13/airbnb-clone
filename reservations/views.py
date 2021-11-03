import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from reviews import forms as review_forms
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users import mixins
from . import models
from .serializers import ReservationListSerializer


class CreateError(Exception):
    pass


@login_required
def create_reservation(request, room, year, month, day, timedelta):
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)

        # 예약 날짜가 있는지 검사
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)

        # 예약 날짜가 있을 경우 고의적 에러 발생.
        raise CreateError()

    # 방이 없을 경우
    except (room_models.Room.DoesNotExist):
        messages.error(request, "The Room doesn't exist")
        return redirect(reverse("core:home"))

    # 예약 날짜가 있을경우
    except CreateError:
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

    # 예약 날짜가 존재 하지 않을 경우.
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=timedelta),
        )

        if not reservation.pk:
            messages.error(request, "Can't Reserve That Room")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationListView(mixins.LoggedInOnlyView, View):
    def get(self, *args, **kwargs):

        # 접속한 유저가 예약 신청한 게스트이거나, 방 주인일때 접속 가능.
        return render(
            self.request,
            "reservations/list.html",
        )


@api_view(["GET"])
def list_reservations(request, noun):

    _status = request.GET.get("status", "all")
    page = int(request.GET.get("page", 1))
    page_size = 12
    limit = page_size * page
    offset = limit - page_size

    if noun == "reserved":
        if _status == "all":
            reservs = models.Reservation.objects.filter(guest=request.user)
        else:
            reservs = models.Reservation.objects.filter(
                guest=request.user, status=_status
            )
    elif noun == "request":
        reservs = models.Reservation.objects.filter(
            room__host=request.user, status="pending"
        )

    reservs_list = reservs.order_by("-created")[offset:limit]
    total_reservs = reservs.count()

    if not reservs:
        return Response(data={"success": False}, status=status.HTTP_404_NOT_FOUND)

    serialized_reservs = ReservationListSerializer(reservs_list, many=True)

    __data = {
        "success": True,
        "data": serialized_reservs.data,
        "total_reservs": total_reservs,
    }

    return Response(data=__data, status=status.HTTP_200_OK)


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)

        # 데이터가 없거나
        # 접속한 유저가 예약 신청한 게스트도 동시에 방 주인이 아닐경우 팅궈냄.
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()

        form = review_forms.CreateReviewForm()

        # 접속한 유저가 예약 신청한 게스트이거나, 방 주인일때 접속 가능.
        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


@login_required
def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)

    # 데이터가 없거나
    # 접속한 유저가 예약 신청한 게스트도 동시에 방 주인이 아닐경우 팅궈냄.
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        messages.error(request, "Invalid Account")
        return redirect(reverse("core:home"))

    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED

    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()

    reservation.save()

    messages.success(request, "Reservation Updated")

    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
