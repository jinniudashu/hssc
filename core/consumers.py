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


from asgiref.sync import sync_to_async
from core.business_functions import update_staff_todo_list 
from core.models import Customer
# 职员任务工作台Consumer，实时更新职员任务列表
class StaffTodoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        operator = await sync_to_async(Customer.objects.get)(user=self.scope['user'])
        await self.channel_layer.group_add(operator.hssc_id, self.channel_name)
        await self.accept()
        
        # 初始化更新职员任务列表
        await sync_to_async(update_staff_todo_list)(operator)

    async def disconnect(self, close_code):
        operator = await sync_to_async(Customer.objects.get)(user=self.scope['user'])
        await self.channel_layer.group_discard(operator.hssc_id, self.channel_name)
        self.close()

    async def send_staff_todo_list(self, event):
        print('StaffTodoConsumer send_staff_todo_list: event[data]', event['data'])
        new_data = event['data']
        await self.send(json.dumps(new_data))


from core.business_functions import update_customer_recommended_service_list 
# 客户服务病例首页Consumer，实时更新客户服务小组的客户各项服务项目
class CustomerRecommendedServicesListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        customer_id = self.scope['url_route']['kwargs']['customer_id']
        await self.channel_layer.group_add(f'customer_recommended_services_{customer_id}', self.channel_name)
        await self.accept()

        # 初始化更新客户可选服务列表
        customer = await sync_to_async(Customer.objects.get)(id=customer_id)
        await sync_to_async(update_customer_recommended_service_list)(customer)

    async def disconnect(self, close_code):
        customer_id = self.scope['url_route']['kwargs']['customer_id']
        await self.channel_layer.group_discard(f'customer_recommended_services_{customer_id}', self.channel_name)
        self.close()

    async def send_customer_recommended_services_list(self, event):
        new_data = event['data']
        await self.send(json.dumps(new_data))


class CustomerServicesListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('CustomerServicesListConsumer connect: self.scope:', self.scope['url_route'])
        # self.scope['url_route']['kwargs']['username']获取url中关键字参数
        customer_id = self.scope['url_route']['kwargs']['customer_id']
        await self.channel_layer.group_add(f'customer_services_{customer_id}', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        customer_id = self.scope['url_route']['kwargs']['customer_id']
        await self.channel_layer.group_discard(f'customer_services_{customer_id}', self.channel_name)
        self.close()

    async def send_customer_services_list(self, event):
        new_data = event['data']
        await self.send(json.dumps(new_data))