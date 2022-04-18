from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q

from core.models import Staff, Customer, OperationProc
from core.forms import OperationFormSet

class OperatorInfo:
    def __init__(self, operator_id):
        self.operator = Staff.objects.get(id=operator_id)
        self.role = self.operator.role.all()

    def get_menu_items(self):
        pass

def index_staff(request):
    context = {}
    # operator=Staff.objects.get(user=request.user)
    # 获取当前用户所属角色组的所有作业进程
    # group = Group.objects.filter(user=request.user)
    user = Staff.objects.get(user=request.user)
    print('user:', user)

    current_operations = OperationProc.objects.current_operations(user)
    print('current_operations:', current_operations)
    current_operations_formset = OperationFormSet(initial=current_operations, prefix='current_operations')
    context['current_procs_formset'] = current_operations_formset

    urgent_operations = OperationProc.objects.urgent_operations(user)
    print('urgent_operations:', urgent_operations)
    urgent_operations_formset = OperationFormSet(initial=urgent_operations, prefix='urgent_operations')
    context['urgent_operations_formset'] = urgent_operations_formset

    week_operations = OperationProc.objects.week_operations(user)
    print('week_operations:', week_operations)
    week_operations_formset = OperationFormSet(initial=week_operations, prefix='week_operations')
    context['week_operations_formset'] = week_operations_formset

    return render(request, 'index_staff.html', context)


def customer_view(request):
    context = {}
    customer = Customer(request.GET.get('customer_id'))
    
    from forms.forms import A6203_ModelForm
    mr_home_page = customer.get_mr_home_page()
    mr_home_page_form = A6203_ModelForm(initial=mr_home_page, prefix='mr_home_page')
    context['mr_home_page_form'] = mr_home_page_form

    from core.forms import OperationItemFormSet
    history_services = customer.get_history_services()
    history_services_formset = OperationItemFormSet(initial=history_services, prefix='history_services')
    context['history_services_formset'] = history_services_formset
    recommanded_services = customer.get_recommanded_services()
    recommanded_services_formset = OperationItemFormSet(initial=recommanded_services, prefix='recommanded_services')
    context['recommanded_services_formset'] = recommanded_services_formset
    scheduled_services = customer.get_scheduled_services()
    scheduled_services_formset = OperationItemFormSet(initial=scheduled_services, prefix='scheduled_services')
    context['scheduled_services_formset'] = scheduled_services_formset

    return render(request, 'customer_info.html', context)


def index_customer(request):
    context = {}
    customer = Customer.objects.get(user=request.user)
    context ['customer'] = customer.name
    print('customer:', customer)
    # 获取当前用户所属的所有作业进程
    procs = OperationProc.objects.exclude(state=4).filter(customer=customer)
    print('procs:', procs)
    todos = []
    for proc in procs:
        todo = {}
        todo['operation'] = proc.operation.label
        todo['url'] = f'{proc.operation.name}_update_url'
        todo['proc_id'] = proc.id
        todos.append(todo)
    context['todos'] = todos

    return render(request, 'index_customer.html', context)


def htmx_test(request):
    print('From htmx_test:', request)
    return HttpResponse('From: htmx_test')
