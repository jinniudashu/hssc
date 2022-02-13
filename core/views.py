from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import ListView
from django.contrib.auth.models import Group
from django.db.models import Q

from core.models import Staff, Operation_proc


def htmx_test(request):
    print('From htmx_test:', request)
    return HttpResponse('From: htmx_test')


class Index_staff(ListView):
    model = Operation_proc
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # 如果用户当前未登录，request.user将被设置为AnonymousUser。用user.is_authenticated()判断用户登录状态：
        # 如果不是员工，则跳转到客户页面
        if not Staff.objects.filter(user=self.request.user).exists():
            return super().get_context_data(**kwargs)
        else:  # 否则，跳转员工页面
            operator=Staff.objects.get(user=self.request.user)
            group = Group.objects.filter(user=self.request.user)
            print('group:', group)
            print('operator:', operator)
            # 获取当前用户所属角色组的所有作业进程
            procs = Operation_proc.objects.exclude(state=4).filter(Q(group__in=group) | Q(operator=operator)).distinct()
            print('procs:', procs)

            todos = []
            for proc in procs:
                todo = {}
                todo['operation'] = proc.operation.label
                todo['url'] = f'{proc.operation.name}_update_url'
                todo['proc_id'] = proc.id
                todos.append(todo)
            context = super().get_context_data(**kwargs)
            context['todos'] = todos
            return context

