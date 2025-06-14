import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PayoutConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = f'payouts_{self.group_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def payout_notification(self, event):
        await self.send(text_data=json.dumps(event['data']))