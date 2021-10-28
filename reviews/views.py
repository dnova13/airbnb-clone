from django.contrib import messages
from django.shortcuts import redirect, reverse
from rooms import models as room_models
from reservations import models as reservation_models
from .serializers import ReviewListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from . import forms


def create_review(request, room_pk, reservation_pk):

    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room_pk)
        reservation = reservation_models.Reservation.objects.get_or_none(
            pk=reservation_pk
        )

        if not room or not reservation:
            return redirect(reverse("core:home"))

        # 리뷰 달았을 경우 팅겨냄
        if reservation.is_reviewed:
            messages.error(request, "Already reviewd")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

        # 유저가 다를 경우 팅겨냄.
        if reservation.guest_id != request.user.pk:
            messages.error(request, "Invalid Account")
            return redirect(reverse("core:home"))

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
        messages.error(request, "Room review failed")
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


@api_view(["GET"])
def list_reviews(request, room_pk):

    page = int(request.GET.get("page", 1))
    page_size = 10
    limit = page_size * page
    offset = limit - page_size

    reviews = Review.objects.filter(room=room_pk).order_by("-created")[offset:limit]
    total_reviews = Review.objects.filter(room=room_pk).count()

    if not reviews:
        return Response(data={"success": False}, status=status.HTTP_404_NOT_FOUND)

    # 직렬화는 기본값이 하나만 하게 되어있기 때문에
    # iterable 객체를 list 같은 객체를 넣을 때는 many를 True로 바꿔줘야함.
    serialized_reviews = ReviewListSerializer(reviews, many=True)

    __data = {
        "success": True,
        "data": serialized_reviews.data,
        "total_reviews": total_reviews,
    }

    return Response(data=__data, status=status.HTTP_200_OK)
