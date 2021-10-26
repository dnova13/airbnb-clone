import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from . import models


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
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
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)

        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        return render(
            self.request, "reservations/detail.html", {"reservation": reservation}
        )
