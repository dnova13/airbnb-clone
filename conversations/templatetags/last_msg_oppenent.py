import datetime
from django import template

register = template.Library()


@register.simple_tag
def last_msg_oppenent(conv, user):
    try:  # 예약된 날짜 존재 유무 체크
        msgs = conv.messages.exclude(user=user)
        lasg_msg = msgs[msgs.count() - 1]

        return lasg_msg
    except Exception:
        return None
