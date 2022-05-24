from django.urls import path

from core.consumers import TestConsumer, StaffTodoConsumer, CustomerRecommendedServicesListConsumer, CustomerServicesListConsumer


ws_urlpatterns = [
    path('ws/core/', TestConsumer.as_asgi()),
    path('ws/staff_todo_list/', StaffTodoConsumer.as_asgi()),
    path('ws/customer_recommended_services_list/', CustomerRecommendedServicesListConsumer.as_asgi()),
    path('ws/customer_services_list/', CustomerServicesListConsumer.as_asgi()),
]