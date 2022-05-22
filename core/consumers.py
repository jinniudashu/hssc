from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('test', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('test', self.channel_name)

    async def send_recommended_service_list(self, event):
        new_data = event['data']
        await self.send(json.dumps(new_data))