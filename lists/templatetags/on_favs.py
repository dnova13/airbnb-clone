from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user

    the_list = list_models.List.objects.get_or_none(
        user=user, name="My Favourites Houses"
    )
    # print(room in the_list.rooms.all())

    return room in the_list.rooms.all()  # 해당 리스트에 요청한 룸이 있으면 true로 반환