from django import template
from lists import models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user

    try:
        orders = models.Order.objects.get(
            list__user=user, list__name="My Favorite Houses", room=room
        )
    except Exception:
        return False

    return True
