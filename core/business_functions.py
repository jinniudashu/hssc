def get_base_fields_name():
    from core.models import HsscFormModel
    # 获取表单基础类
    base_fields_name = {field.name for field in HsscFormModel._meta.fields}
    return base_fields_name.add('id')

def copy_previous_form_data(form):
    # 获取父进程表单
    previous_form = form.pid.parent_proc.content_object
    # 获取父进程表单和当前进程表单字段的交集
    base_fields_name = get_base_fields_name()  # 表单基础字段集合
    previous_form_fields_name = {field.name for field in previous_form._meta.fields} - base_fields_name
    form_fields_name = {field.name for field in form._meta.fields} - base_fields_name
    copy_fields_name = previous_form_fields_name.intersection(form_fields_name)

    previous_form_fields_name_m2m = {field.name for field in previous_form._meta.many_to_many}
    form_fields_name_m2m = {field.name for field in form._meta.many_to_many}
    copy_fields_name_m2m = previous_form_fields_name_m2m.intersection(form_fields_name_m2m)

    # 向当前进程表单写入交集字段内容
    for field_name in copy_fields_name:
        print(field_name, '值：', eval(f'previous_form.{field_name}'))
        eval(f'form.{field_name} = previous_form.{field_name}')
    form.save()

    # 向当前进程表单写入交集多对多字段内容
    for field_name in copy_fields_name_m2m:
        print(field_name, '值：', eval(f'previous_form.{field_name}.all()'))
        for obj in eval(f'previous_form.{field_name}.all()'):
            eval(f'form.{field_name}.add(obj)')

    return form


from service.models import *
# 创建服务表单实例
def create_form_instance(operation_proc, passing_data):
    # 1. 创建空表单
    model_name = operation_proc.service.name.capitalize()
    form_instance = eval(model_name).objects.create(
        customer=operation_proc.customer,
        creater=operation_proc.operator,
        pid=operation_proc,
        cpid=operation_proc.contract_service_proc,
    )
    print('From service.models.create_form_instance, 创建表单实例:', model_name, form_instance)

    # 2. 如果不是基本信息表作业(作业服务表单!=作业服务的实体基本信息表单)，则为属性表，填入表头字段
    service = operation_proc.service
    if service.buessiness_forms.all().first() != service.managed_entity.base_form:
        # 判断当前实体，填入实体基本信息表头字段
        # 通用代码里customer应改为entity
        base_info = eval(service.managed_entity.base_form.service_set.all().first().name.capitalize()).objects.filter(customer=operation_proc.customer).first()
        # *********以下应为生成代码！生成所属实体表头信息************
        form_instance.characterfield_family_address = base_info.characterfield_family_address
        form_instance.characterfield_contact_number = base_info.characterfield_contact_number
        form_instance.characterfield_name = base_info.characterfield_name
        form_instance.relatedfield_gender = base_info.relatedfield_gender
        form_instance.datetimefield_date_of_birth = base_info.datetimefield_date_of_birth
        form_instance.save()

    # 3. 如果passing_data>0, copy父进程表单数据
    if passing_data > 0:  # passing_data: 传递表单数据：(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')
        copy_previous_form_data(form_instance)

    return form_instance


# 创建服务进程实例
def create_service_proc(**kwargs):
    from core.models import OperationProc
    # 创建新的服务作业进程
    new_proc=OperationProc.objects.create(
        service=kwargs['service'],
        customer=kwargs['customer'],
        creater=kwargs['creater'],
        operator=kwargs['operator'],
        state=kwargs['state'],
        scheduled_time=kwargs['scheduled_time'],
        parent_proc=kwargs['parent_proc'],
        contract_service_proc=kwargs['contract_service_proc'],
        content_type=kwargs['content_type'],
    )
    # Here postsave signal in service.models
    # 更新允许作业岗位
    role = kwargs['service'].role.all()
    new_proc.role.set(role)

    form = create_form_instance(new_proc, kwargs['passing_data'])
    # 更新OperationProc服务进程的form实例信息
    new_proc.object_id = form.id
    new_proc.entry = f'/clinic/service/{new_proc.service.name.lower()}/{form.id}/change'
    new_proc.save()

    return new_proc


from core.hsscbase_class import FieldsType
# 创建客户服务日志：把服务表单内容写入客户服务日志
def create_customer_service_log(post_data, form_instance):
    from enum import Enum
    from core.models import CustomerServiceLog
    # 数据格式预处理
    def _preprocess_data_format(post_data):
        def _get_set_value(field_type, id_list):
            print('field_type:', field_type, 'id_list:', id_list)
            # 转换id列表为对应的字典值列表
            _model_list = field_type.split('.')  # 分割模型名称field_type: app_label.model_name
            app_label = _model_list[0]  # 应用名称
            model_name = _model_list[1]  # 模型名称
            class ConvertIdToValue(Enum):
                icpc = map(lambda x: eval(model_name).objects.get(id=x).iname, id_list)
                dictionaries = map(lambda x: eval(model_name).objects.get(id=x).value, id_list)
                service = map(lambda x: eval(model_name).objects.get(id=x).name, id_list)
                core = map(lambda x: eval(model_name).objects.get(id=x).name, id_list)
            val_iterator = eval(f'ConvertIdToValue.{app_label}').value
            return f'{set(val_iterator)}'

        post_data.pop('csrfmiddlewaretoken')
        post_data.pop('_save')
        form_data = {**post_data}  # 把QuerySet对象转为Dict
        for field_name, field_val in form_data.items():
            print('field_name:', field_name, 'field_val:', field_val)
            # 根据字段类型做字段值的格式转换
            field_type = eval(f'FieldsType.{field_name}').value
            if field_type == 'Datetime' or field_type == 'Date':  # 日期类型暂时不处理
                form_data[field_name] = f'{field_val}'
            elif field_type == 'Numbers':  # 如果字段类型是Numbers，直接使用字符串数值
                form_data[field_name] = field_val[0]
            elif field_type == 'String':  # 如果字段类型是String，转换为集合字符串
                form_data[field_name] = f'{set(field_val)}' if field_val and field_val!=[''] else '{}'
            else:  # 如果字段类型是关联字段，转换为集合字符串
                form_data[field_name] = _get_set_value(field_type, field_val) if field_val and field_val!=['']  else '{}'
        return form_data

    def _add_customer_service_log(form_data, form_instance):
        from django.core.exceptions import ObjectDoesNotExist
        try:
            log = CustomerServiceLog.objects.get(pid = form_instance.pid)
            log.data = form_data
            log.save()
        except ObjectDoesNotExist:
            log = CustomerServiceLog.objects.create(
                name=form_instance.name,
                label=form_instance.label,
                customer=form_instance.customer,
                operator=form_instance.operator,
                creater=form_instance.creater,
                pid=form_instance.pid,
                cpid=form_instance.cpid,
                data=form_data,
            )
        return log

    _form_data = _preprocess_data_format(post_data)
    log = _add_customer_service_log(_form_data, form_instance)

    return log

# 获取客户基本信息
def get_customer_profile(customer):
    instance = Ju_min_ji_ben_xin_xi_diao_cha.objects.filter(customer=customer).last()

    url = f'/clinic/service/ju_min_ji_ben_xin_xi_diao_cha/{instance.id}/change'

    profile = {
        'name': instance.characterfield_name,
        'phone': instance.characterfield_contact_number,
        'address': instance.characterfield_family_address,
        'charge_staff': instance.relatedfield_signed_family_doctor,
        'workgroup': instance.customer.workgroup.label if instance.customer.workgroup else '',
        'url': url,
    }

    return profile


# 为新服务分配操作员
def dispatch_operator(customer, service, current_operator):
    from django.core.exceptions import ObjectDoesNotExist
    operator = None

    # 当前客户如有责任人，且责任人具有新增服务岗位权限，则开单给责任人
    charge_staff = customer.charge_staff
    if charge_staff:
        if set(charge_staff.staff.role.all()).intersection(set(service.role.all())):
            operator = charge_staff
            return operator
    
    # 否则，如当前作业员具有新增服否则，如当前作业员具有新增服务岗位权限务岗位权限
    try:
        if set(current_operator.staff.role.all()).intersection(set(service.role.all())):
            operator = current_operator
            return operator
    except ObjectDoesNotExist:
        return None

    # 否则，操作员为空，进入共享队列
    return None


# 获取操作员有操作权限的服务id列表
def get_operator_permitted_services(operator):
    from core.models import Service
    return [
        service.id
        for service in Service.objects.filter(is_system_service=False) 
        if set(service.role.all()).intersection(set(operator.staff.role.all()))
    ]


# 发送channel_message
def send_channel_message(group_name, message):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    print('发送channel信号:', group_name, message)
    async_to_sync(channel_layer.group_send)(group_name, message)

from core.models import OperationProc
def update_unassigned_procs():
    # 可申领的服务作业
    unassigned_procs = {
        'unassignedProcs': [
            {
                'id': proc.id,
                'service_id': proc.service.id,
                'service_name': proc.service.label,
                'customer_name': proc.customer.name,
                'workgroup_name': proc.customer.workgroup.label if proc.customer.workgroup else '',
            } for proc in OperationProc.objects.filter(state=0, operator=None)
        ]
    }

    # 发送channel_message给操作员
    send_channel_message('unassigned_procs', {'type': 'send_unassigned_procs', 'data': unassigned_procs})

from core.models import StaffTodo
# 更新工作台职员任务列表
def update_staff_todo_list(operator):
    # 根据operator过滤出操作员的今日安排、紧要安排、本周安排
    layout_items = [
        {'title': '今日服务安排', 'todos': StaffTodo.objects.today_todos(operator)},
        {'title': '紧要服务安排', 'todos': StaffTodo.objects.urgent_todos(operator)},
        {'title': '本周服务安排', 'todos': StaffTodo.objects.week_todos(operator)},
    ]

    # 构造channel_message items
    items = []
    for _item in layout_items:
        todos = []
        for todo in _item['todos']:
            todos.append({
                'id': todo.id,
                'customer_id': todo.operation_proc.customer.id,
                'customer_number': todo.customer_number,
                'customer_name': todo.customer_name,
                'service_label': todo.service_label,
                'customer_phone': todo.customer_phone,
                'customer_address': todo.customer_address,
            })
        items.append({'title': _item['title'], 'todos': todos})

    # 发送channel_message给操作员
    send_channel_message(operator.hssc_id, {'type': 'send_staff_todo_list', 'data': items})

# 更新客户服务列表
def update_customer_services_list(customer):
    # 已安排服务
    scheduled_services = [
        {
            'service_entry': proc.entry,
            'service_name': proc.service.label,
            'service_id': proc.service.id,
        } for proc in customer.get_scheduled_services()
    ]

    # 历史服务
    history_services =  [
        {
            'service_entry': proc.entry,
            'service_name': proc.service.label,
            'service_id': proc.service.id,
        } for proc in customer.get_history_services()
    ]

    servicesList = {
        'scheduled_services': scheduled_services,
        'history_services': history_services,
    }
    # 发送channel_message给操作员
    send_channel_message(f'customer_services_{customer.id}', {'type': 'send_customer_services_list', 'data': servicesList})

# 更新客户推荐服务项目列表
def update_customer_recommended_services_list(customer):
    # # 推荐服务
    recommendedServices = [
        {
            'id': recommend_service.id,
            'customer_id': customer.id,
            'service_id': recommend_service.service.id,
            'service_name': recommend_service.service.label,
            'enable_queue_counter': recommend_service.service.enable_queue_counter,
            'queue_count': OperationProc.objects.get_service_queue_count(recommend_service.service),
            'counter': recommend_service.counter,
        } for recommend_service in customer.get_recommended_services()
    ]

    # 发送channel_message给操作员
    send_channel_message(f'customer_recommended_services_{customer.id}', {'type': 'send_customer_recommended_services_list', 'data': recommendedServices})


from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@receiver(post_save, sender=StaffTodo)
def staff_todo_post_save_handler(sender, instance, created, **kwargs):
    # 根据operator过滤出操作员的今日安排、紧要安排、本周安排
    update_staff_todo_list(instance.operator)

@receiver(post_delete, sender=StaffTodo)
def staff_todo_post_delete_handler(sender, instance, **kwargs):
    # 根据operator过滤出操作员的今日安排、紧要安排、本周安排
    update_staff_todo_list(instance.operator)

from core.models import RecommendedService

@receiver(post_save, sender=RecommendedService)
def recommended_service_post_save_handler(sender, instance, created, **kwargs):
    # 根据customer过滤出用户的可选服务，发送channel_message给“用户服务组”
    update_customer_recommended_services_list(instance.customer)

@receiver(post_delete, sender=RecommendedService)
def recommended_service_post_delete_handler(sender, instance, **kwargs):
    # 根据customer过滤出用户的可选服务，发送channel_message给“用户服务组”
    update_customer_recommended_services_list(instance.customer)


# **********************************************************************************************************************
# KMP算法：查找字段名在表达式（字符串）中的位置，并用字段值替换
# **********************************************************************************************************************
def field_name_replace(s, replace_dict):
    import re
    next = []
    changed_str = s

    def buildNext():
        next.append(0)
        x = 1
        now = 0
        while x < len(p):
            if p[now] == p[x]:
                now += 1
                x += 1
                next.append(now)
            elif now:
                now = next[now-1]
            else:
                next.append(0)
                x += 1

    def search(new_str):
        tar = 0
        pos = 0
        while tar < len(s):
            if s[tar] == p[pos]:
                tar += 1
                pos += 1
            elif pos:
                pos = next[pos-1]
            else:
                tar += 1
            if pos == len(p):   # 匹配成功
                next_str = re.sub(p, replace_dict[p], new_str)
                pos = next[pos-1]
                return next_str

    for p in replace_dict:
        buildNext()
        changed_str = search(changed_str)

    return changed_str

# KMP算法：查找字典中的关键词在字符串中的位置
def keyword_search(s, keywords_list):
    next = []
    match = []

    def buildNext():
        next.append(0)
        x = 1
        now = 0
        while x < len(p):
            if p[now] == p[x]:
                now += 1
                x += 1
                next.append(now)
            elif now:
                now = next[now-1]
            else:
                next.append(0)
                x += 1

    def search():
        tar = 0
        pos = 0
        while tar < len(s):
            if s[tar] == p[pos]:
                tar += 1
                pos += 1
            elif pos:
                pos = next[pos-1]
            else:
                tar += 1
            if pos == len(p):   # 匹配成功
                match.append(p)
                pos = next[pos-1]

    for p in keywords_list:
        buildNext()
        search()
    keywords = sorted(set(match), key=match.index)
    return keywords
