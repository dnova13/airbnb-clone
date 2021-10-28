from django.contrib import messages
from django.shortcuts import redirect, reverse
from rooms import models as room_models
from reservations import models as reservation_models
from . import forms


def create_review(request, room, reservation):

    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        reservation = reservation_models.Reservation.objects.get_or_none(pk=reservation)

        if not room or not reservation:
            return redirect(reverse("core:home"))

        # 리뷰 달았을 경우 팅겨냄
        if reservation.is_reviewed:
            messages.success(request, "Already reviewd")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user

            reservation.is_reviewed = True

            review.save()
            reservation.save()

            messages.success(request, "Room reviewed")

            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

        # 실패 햇을 경우.
        messages.success(request, "Room review failed")
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
