from django import template
from lists import models

register = template.Library()


@register.simple_tag
def fav_count(user):

    orders = models.Order.objects.filter(
        list__user=user, list__name="My Favorite Houses"
    )

    return orders.count() if orders else 0
