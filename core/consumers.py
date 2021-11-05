from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
import json


class NotiConsumer(AsyncWebsocketConsumer):

    # connect : 사용자와 websocket 연결이 맺어졌을때 호출
    async def connect(self):
        self.user_pk = self.scope["url_route"]["kwargs"]["user_pk"]
        self.conv_group_name = "noti_%s" % self.user_pk

        await self.channel_layer.group_add(self.conv_group_name, self.channel_name)
        await self.accept()

    # disconnect : 사용자와 websocket 연결이 끊겼을때 호출
    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.conv_group_name, self.channel_name)

    # receive : 사용자가 보낸 메시지를 보내면 그걸 받아서 호출
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        await self.channel_layer.group_send(
            self.conv_group_name, {"type": "notice_message", "message": message}
        )

    # 그리고 받은 메세지를 다른 상대에게 호출
    async def notice_message(self, event):

        # event 에서 위에서 보낸 데이터 {"type": "notice_message", "message": message} 받음
        message = event["message"]
        print(message)

        await self.send(text_data=json.dumps({"message": message}, default=str))
