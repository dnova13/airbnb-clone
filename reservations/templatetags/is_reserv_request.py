from typing import Tuple
from django import template
from reservations import models

register = template.Library()


""" reservs = models.Reservation.objects.filter(
            room__host=request.user, status="pending"
        ) """


@register.simple_tag
def is_reserv_request(user):
    try:
        reservs = models.Reservation.objects.filter(room__host=user, status="pending")
        return reservs.count() > 0

    except Exception:
        return None
