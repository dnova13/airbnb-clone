import json
from django.contrib import messages
from django.db.models import Q
from django.db.models.query_utils import PathInfo
from django.http import Http404
from django.shortcuts import redirect, reverse, render
from django.views.generic import View
from users import models as user_models
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models, forms, serializers
from users import mixins


def get_or_none(user_pk):

    try:
        return user_models.User.objects.get(pk=user_pk)
    except user_models.DoesNotExist:
        return None


@login_required
def go_conversation(request, a_pk, b_pk):

    user_one = get_or_none(user_pk=a_pk)
    user_two = get_or_none(user_pk=b_pk)

    if request.user.pk != a_pk and request.user.pk != b_pk:
        messages.error(request, "Invalid Account")
        return redirect(reverse("core:home"))

    if user_one is not None and user_two is not None:

        conversation = models.Conversation.objects.filter(participants=user_one).filter(
            participants=user_two
        )

        if conversation.count() == 0:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)

        return redirect(
            reverse("conversations:detail", kwargs={"pk": conversation[0].pk})
        )

    else:
        messages.error(request, "Invalid Account")
        return redirect(reverse("core:home"))


class ConversationListView(View):
    def get(self, *args, **kwargs):
        conversation = models.Conversation.objects.filter(
            participants=self.request.user
        )

        return render(
            self.request,
            "conversations/conversation_list.html",
            {"conversation": conversation},
        )


class ConversationDetailView(mixins.LoggedInOnlyView, View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        conversation.is_over_messges()

        if not conversation:
            messages.error(self.request, "cant' go there")
            return redirect(reverse("core:home"))

        valid_chk = False

        for i, user in enumerate(conversation.participants.all()):
            if user.id == self.request.user.pk:
                valid_chk = True
                me = user
                idx = i
                break

        if not valid_chk:
            messages.error(self.request, "Invalid Account")
            return redirect(reverse("core:home"))

        opponent = (
            conversation.participants.all()[0]
            if idx == 1
            else conversation.participants.all()[1]
        )

        conversation.messages.filter(user=opponent, is_read=False).update(is_read=True)
        conv_messages = conversation.messages.order_by("-id")[0:20]

        return render(
            self.request,
            "conversations/conversation_detail.html",
            {
                "conversation": conversation,
                "me": me,
                "opponent": opponent,
                "conv_messages": conv_messages,
            },
        )

    """ def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)

        if not conversation:
            messages.error(self.request, "cant' go there")
            return redirect(reverse("core:home"))

        valid_chk = False

        for participant in conversation.participants.all():
            if participant.id == self.request.user.pk:
                valid_chk = True
                break

        if not valid_chk:
            messages.error(self.request, "Invalid Account")
            return redirect(reverse("core:home"))

        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )

        return redirect(reverse("conversations:detail", kwargs={"pk": pk})) """


@api_view(["GET"])
def get_msgs(request, pk):
    conversation = models.Conversation.objects.get_or_none(pk=pk)

    page_size = 15

    offset = int(request.GET.get("start", 1)) - 1
    limit = page_size + offset

    if offset < 0:
        messages.error(request, "cant' go there")
        return Response(data={"success": False}, status=status.HTTP_401_UNAUTHORIZED)

    if not conversation:
        messages.error(request, "cant' go there")
        return Response(data={"success": False}, status=status.HTTP_401_UNAUTHORIZED)

    valid_chk = False

    for participant in conversation.participants.all():
        if participant.id == request.user.pk:
            valid_chk = True
        else:
            opponent = participant

    if not valid_chk:
        messages.error(request, "Invalid Account")
        return Response(data={"success": False}, status=status.HTTP_401_UNAUTHORIZED)

    conversation.messages.filter(user=opponent, is_read=False).update(is_read=True)

    total_msgs = conversation.messages.count()
    conv_msgs = conversation.messages.order_by("-id")[offset:limit]

    if not conv_msgs:
        return Response(data={"success": False}, status=status.HTTP_204_NO_CONTENT)

    serialized_msgs = serializers.MessagesSerializer(conv_msgs, many=True)

    __data = {
        "success": True,
        "data": serialized_msgs.data,
        "total_msgs": total_msgs,
    }

    return Response(data=__data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_msg(request, pk):

    _data = request.data

    conversation = models.Conversation.objects.get_or_none(pk=pk)

    if not ("msg" in _data):
        messages.error(request, "cant' go there")
        return Response(data={"success": False}, status=status.HTTP_401_UNAUTHORIZED)

    if not conversation:
        messages.error(request, "cant' go there")
        return Response(data={"success": False}, status=status.HTTP_401_UNAUTHORIZED)

    valid_chk = False

    for participant in conversation.participants.all():
        if participant.id == request.user.pk:
            valid_chk = True
            break

    if not valid_chk:
        messages.error(request, "Invalid Account")
        return Response(data={"success": False}, status=status.HTTP_401_UNAUTHORIZED)

    msg_obj = models.Message.objects.create(
        message=_data["msg"], user=request.user, conversation=conversation
    )

    _data = {
        "data": {"created": msg_obj.created, "is_read": msg_obj.is_read},
    }

    return Response(data={"success": True, "data": _data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def read_msg(request, pk):

    conversation = models.Conversation.objects.get_or_none(pk=pk)

    if not conversation:
        messages.error(request, "cant' go there")
        return Response(data={"success": False}, status=status.HTTP_401_UNAUTHORIZED)

    valid_chk = False

    for participant in conversation.participants.all():
        if participant.id == request.user.pk:
            valid_chk = True
            me = participant
        else:
            opponent = participant

    if not valid_chk:
        messages.error(request, "Invalid Account")
        return Response(data={"success": False}, status=status.HTTP_401_UNAUTHORIZED)

    conversation.messages.filter(user=opponent, is_read=False).update(is_read=True)

    return Response(data={"success": True}, status=status.HTTP_200_OK)
