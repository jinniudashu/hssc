from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.contrib import admin
from django.contrib.auth.models import User

from core.models import OperationProc, StaffTodo, Customer

class ClinicSite(admin.AdminSite):
    site_header = '智益诊所管理系统'
    site_title = 'Hssc Clinic'
    index_title = '诊所工作台'
    enable_nav_sidebar = False
    index_template = 'admin/index_clinic.html'
    enable_nav_sidebar = False
    site_url = None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('receive_task/<int:proc_id>', self.receive_task),
            path('customer_service/<int:customer_id>', self.customer_service),
        ]
        return my_urls + urls

    # 职员登录后的首页
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        user = User.objects.get(username=request.user).customer
        # 可申领的服务作业
        extra_context['unassigned_procs'] = OperationProc.objects.get_unassigned_proc(user)
        # 今日服务安排,紧要服务安排,本周服务安排
        items = []
        items.append({'title': '今日服务安排', 'todos': StaffTodo.objects.today_todos(user)})
        items.append({'title': '紧要服务安排', 'todos': StaffTodo.objects.urgent_todos(user)})
        items.append({'title': '本周服务安排', 'todos': StaffTodo.objects.week_todos(user)})
        extra_context['items'] = items

        return super().index(request, extra_context=extra_context)

    # 接受任务：把任务放入当前用户的待办列表中
    def receive_task(self, request, **kwargs):
        operation_proc = OperationProc.objects.get(id = kwargs['proc_id'])
        operation_proc.operator = User.objects.get(username=request.user).customer
        operation_proc.state = 1
        operation_proc.save()
        return redirect('/clinic/')
        

    # 客户服务首页
    def customer_service(self, request, **kwargs):
        context = {}
        customer = Customer.objects.get(id = kwargs['customer_id'])
        
        context['profile'] = customer.get_profile()  # 病例首页
        context['history_services'] = customer.get_history_services()  # 历史服务
        context['recommanded_services'] = customer.get_recommanded_services()  # 推荐服务
        context['scheduled_services'] = customer.get_scheduled_services()  # 已安排服务

        return render(request, 'customer_service.html', context)

clinic_site = ClinicSite(name = 'ClinicSite')
