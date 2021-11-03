from typing import Tuple
from django import template
from conversations import models

register = template.Library()


@register.simple_tag
def is_msgs_read(user):
    try:
        convs = models.Conversation.objects.filter(participants=user)
        for cov in convs:
            msg_obj = cov.messages.exclude(user=user).filter(is_read="False")

            if msg_obj:
                return True

        return False

    except Exception:
        return None
