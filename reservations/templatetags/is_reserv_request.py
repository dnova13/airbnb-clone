from typing import Tuple
from django import template
from reservations import models

register = template.Library()


@register.simple_tag
def is_reserv_request(user):
    try:
        reservs = models.Reservation.objects.filter(room__host=user)

        return reservs.count() > 0

    except Exception:
        return False
