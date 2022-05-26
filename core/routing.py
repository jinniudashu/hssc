from django.urls import path

from core.consumers import UnassignedProcsConsumer, StaffTodoConsumer, CustomerRecommendedServicesListConsumer, CustomerServicesListConsumer


ws_urlpatterns = [
    path('ws/unassigned_procs/', UnassignedProcsConsumer.as_asgi()),
    path('ws/staff_todos_list/', StaffTodoConsumer.as_asgi()),
    path('ws/customer_recommended_services_list/<int:customer_id>/', CustomerRecommendedServicesListConsumer.as_asgi()),
    path('ws/customer_services_list/<int:customer_id>/', CustomerServicesListConsumer.as_asgi()),
]