from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.views.generic import DetailView
from users import models as user_models
from django.contrib.auth.decorators import login_required
from . import models


def get_or_none(user_pk):
    try:
        return user_models.User.objects.get(pk=user_pk)
    except user_models.DoesNotExist:
        return None


@login_required
def go_conversation(request, a_pk, b_pk):

    user_one = get_or_none(user_pk=a_pk)
    user_two = get_or_none(user_pk=b_pk)

    if user_one is not None and user_two is not None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )

        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)

        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(DetailView):

    model = models.Conversation
