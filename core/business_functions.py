def copy_previous_form_data(form, previous_form_data):
    # 获取父进程表单
    
    if form.pid.parent_proc:
        previous_form = form.pid.parent_proc.content_object
    else:
        previous_form = None

    if previous_form:
        # 如果有父进程表单，获取父进程表单字段
        from core.models import HsscFormModel
        # 获取父进程表单和当前进程表单字段的交集
        base_fields_name = {field.name for field in HsscFormModel._meta.fields}  # 表单基础字段集合
        base_fields_name.add('id')

        previous_form_fields_name = {field.name for field in previous_form._meta.fields} - base_fields_name
        form_fields_name = {field.name for field in form._meta.fields} - base_fields_name
        copy_fields_name = previous_form_fields_name.intersection(form_fields_name)

        previous_form_fields_name_m2m = {field.name for field in previous_form._meta.many_to_many}
        form_fields_name_m2m = {field.name for field in form._meta.many_to_many}
        copy_fields_name_m2m = previous_form_fields_name_m2m.intersection(form_fields_name_m2m)
    else:
        # 否则是外部进程表单，获取表单字段
        copy_fields_name_m2m = {field.name for field in form._meta.many_to_many}
        copy_fields_name = {key for key in previous_form_data.keys()} - copy_fields_name_m2m

    # 向当前进程表单写入交集字段内容
    for field_name in copy_fields_name:
        field_value = previous_form_data.get(field_name)
        if field_value:
            exec(f'form.{field_name} = field_value')
    form.save()

    # 向当前进程表单写入交集多对多字段内容
    for field_name in copy_fields_name_m2m:
        m2m_objs = previous_form_data.get(field_name)
        # 如果m2m_objs不是列表类型，转换为列表类型，以适配外部表单copy_form_data
        if not isinstance(m2m_objs, list):
            m2m_objs = [m2m_objs]

        if m2m_objs:
            exec(f'form.{field_name}.add(*m2m_objs)')

    return form


from service.models import *
# 创建服务表单实例
def create_form_instance(operation_proc, passing_data, form_data):
    # 1. 创建空表单
    model_name = operation_proc.service.name.capitalize()
    form_instance = eval(model_name).objects.create(
        customer=operation_proc.customer,
        creater=operation_proc.operator,
        pid=operation_proc,
        cpid=operation_proc.contract_service_proc,
    )

    # 2. 如果不是基本信息表作业(作业服务表单!=作业服务的实体基本信息表单)，则为属性表，填入表头字段
    # service = operation_proc.service
    # if service.buessiness_forms.all().first() != service.managed_entity.base_form:
    #     # 判断当前实体，填入实体基本信息表头字段
    #     # 通用代码里customer应改为entity
    #     base_info = eval(service.managed_entity.base_form.service_set.all().first().name.capitalize()).objects.filter(customer=operation_proc.customer).first()
    #     # *********以下应为生成代码！生成所属实体表头信息************
    #     form_instance.boolfield_chang_zhu_di_zhi = base_info.boolfield_chang_zhu_di_zhi
    #     # form_instance.characterfield_contact_number = base_info.boolfield_lian_xi_dian_hua
    #     form_instance.characterfield_name = base_info.characterfield_name
    #     form_instance.characterfield_gender = base_info.characterfield_gender
    #     form_instance.datetimefield_date_of_birth = base_info.datetimefield_date_of_birth
    #     form_instance.save()

    # 3. 如果passing_data>0, copy父进程表单数据
    if passing_data > 0 and form_data:  # passing_data: 传递表单数据：(0, '否'), (1, '接收，不可编辑', 复制父进程表单控制信息), (2, '接收，可以编辑', 复制父进程表单控制信息), (3, 复制form_data)
        copy_previous_form_data(form_instance, form_data)

    return form_instance


# 创建服务进程实例
def create_service_proc(**kwargs):
    import json
    # 检查父进程表单是否携带进程控制信息(检查api_fields字段)，如果有，整合所有表单的进程控制信息(charge_staff, operator, scheduled_time)
    # 提取进程控制信息，更新相应控制项内容。Api_field = [('charge_staff', '责任人'), ('operator', '作业人员'), ('scheduled_time', '计划执行时间')]
    form_data = kwargs['form_data']
    if kwargs['passing_data'] in [1, 2]:
        # 获取父进程中api_fields不为空的表单, 并获取其中的进程控制信息api_fields
        _forms = [form for form in kwargs['parent_proc'].service.buessiness_forms.all() if form.api_fields]
        api_fields = []
        for _form in _forms:
            api_fields.extend(json.loads(_form.api_fields))
        # 逐一获取api接口字段的值，赋给相应控制字段
        for api_field in api_fields:
            for system_field, form_field in api_field.items():
                if form_data.get(form_field):
                    if system_field == 'operator':  # operator: 作业人员                    
                        operator = form_data.get(form_field).customer
                        kwargs['operator'] = operator
                    elif system_field == 'scheduled_time':  # scheduled_time: 计划执行时间
                        scheduled_time = form_data.get(form_field)
                        kwargs['scheduled_time'] = scheduled_time
                    elif system_field=='charge_staff':  # charge_staff: 责任人
                        charge_staff = form_data.get(form_field).customer
                        kwargs['customer'].charge_staff = charge_staff
                        kwargs['customer'].save()                        
                    else:
                        pass

    # 创建新的服务作业进程
    from core.models import OperationProc
    parent_proc=kwargs.get('parent_proc')
    if parent_proc:
        new_proc=OperationProc.objects.create(
            service=kwargs['service'],
            customer=kwargs['customer'],
            creater=kwargs['creater'],
            operator=kwargs['operator'],
            state=kwargs['state'],
            scheduled_time=kwargs['scheduled_time'],
            parent_proc=parent_proc,
            contract_service_proc=kwargs.get('contract_service_proc'),
            content_type=kwargs['content_type'],
        )
    else:
        new_proc=OperationProc.objects.create(
            service=kwargs['service'],
            customer=kwargs['customer'],
            creater=kwargs['creater'],
            operator=kwargs['operator'],
            state=kwargs['state'],
            scheduled_time=kwargs['scheduled_time'],
            contract_service_proc=kwargs.get('contract_service_proc'),
            content_type=kwargs['content_type'],
        )
    # Here postsave signal in service.models
    # 更新允许作业岗位
    role = kwargs['service'].role.all()
    new_proc.role.set(role)

    form = create_form_instance(new_proc, kwargs['passing_data'], form_data)
    # 更新OperationProc服务进程的form实例信息
    new_proc.object_id = form.id
    new_proc.entry = f'/clinic/service/{new_proc.service.name.lower()}/{form.id}/change'
    new_proc.save()

    return new_proc


# 创建客户服务日志：把服务表单内容写入客户服务日志
def create_customer_service_log(form_data, form_instance):
    from django.db.models.query import QuerySet
    from django.core.exceptions import ObjectDoesNotExist
    from core.models import CustomerServiceLog
    from core.hsscbase_class import FieldsType

    def _get_set_value(field_type, id_list):
        # 转换id列表为对应的字典值列表
        app_label = field_type.split('.')[0]  # 分割模型名称field_type: app_label.model_name，获得应用名称
        val_iterator = []
        if isinstance(id_list, QuerySet):
            if app_label == 'icpc':
                val_iterator = map(lambda x: x.iname, id_list)
            elif app_label == 'dictionaries':
                val_iterator = map(lambda x: x.value, id_list)
            else:
                val_iterator = map(lambda x: x.name, id_list)
        else:
            if app_label == 'icpc':
                val_iterator = [id_list.iname]
            elif app_label == 'dictionaries':
                val_iterator = [id_list.value]
            else:
                val_iterator = [id_list.name]
        return f'{set(val_iterator)}'

    # 数据格式预处理
    for field_name, field_val in form_data.items():
        # 根据字段类型做字段值的格式转换
        field_type = eval(f'FieldsType.{field_name}').value
        if field_type == 'Datetime' or field_type == 'Date':  # 日期类型暂时不处理
            form_data[field_name] = f'{field_val}'
        elif field_type == 'Numbers':  # 如果字段类型是Numbers，直接使用字符串数值
            form_data[field_name] = str({field_val}) if field_val != None else '{}'
        elif field_type == 'String':  # 如果字段类型是String，转换为集合字符串
            form_data[field_name] = str({field_val}) if field_val and field_val!=[''] else '{}'
        else:  # 如果字段类型是关联字段，转换为集合字符串
            form_data[field_name] = _get_set_value(field_type, field_val) if field_val and field_val!=['']  else '{}'

    print('完成预处理form_data:', form_data)
    # 保存form_data
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


# 获取客户基本信息
def get_customer_profile(customer):
    from core.models import ManagedEntity
    from service.forms import Ju_min_ji_ben_xin_xi_diao_cha_HeaderForm
    # 获取客户的基本信息表单
    base_form = ManagedEntity.objects.get(name='customer').base_form
    base_form_service_name = base_form.service_set.all().first().name
    instance = eval(f'{base_form_service_name.capitalize()}.objects.filter(customer=customer).last()')
    header_form = eval(f'{base_form_service_name.capitalize()}_HeaderForm(instance=instance)')
    url = f'/clinic/service/{base_form_service_name}/{instance.id}/change'
    profile = {
        'id': customer.id,
        'charge_staff': '',
        'workgroup': instance.customer.workgroup.label if instance.customer.workgroup else '',
        'url': url,
        'form': header_form,
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
    
    # 否则，如当前作业员具有新增服务岗位权限务岗位权限，则开单给作业员
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
    async_to_sync(channel_layer.group_send)(group_name, message)


from core.models import OperationProc
def update_unassigned_procs():
    # 可申领的服务作业
    unassigned_procs = {
        'unassignedProcs': [
            {
                'id': proc.id,
                'service_id': proc.service.id,
                'service_label': proc.service.label,
                'customer_name': proc.customer.name,
                'workgroup_name': proc.customer.workgroup.label if proc.customer.workgroup else '',
                'acceptance_timeout': proc.acceptance_timeout,
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
                'completion_timeout': todo.operation_proc.completion_timeout,
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
            'service_label': proc.service.label,
            'service_id': proc.service.id,
            'completion_timeout': proc.completion_timeout,
        } for proc in customer.get_scheduled_services()
    ]

    # 历史服务
    history_services =  [
        {
            'service_entry': proc.entry,
            'service_label': proc.service.label,
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
            'service_label': recommend_service.service.label,
            'enable_queue_counter': recommend_service.service.enable_queue_counter,
            'queue_count': OperationProc.objects.get_service_queue_count(recommend_service.service),
            'counter': recommend_service.counter,
        } for recommend_service in customer.get_recommended_services()
    ]

    # 发送channel_message给操作员
    send_channel_message(f'customer_recommended_services_{customer.id}', {'type': 'send_customer_recommended_services_list', 'data': recommendedServices})


# 把客户服务项目安排转为客户服务日程
def get_services_schedule(instances):
    def _get_schedule_times(instance, first_start_time, previous_end_time):
        # 返回: 计划时间列表
        def _add_base_interval(time, interval):
            if interval:
                time = time + interval
            return time
            
        unit_days = instance.cycle_unit.days  # 周期单位天数
        cycle_frequency = instance.cycle_frequency  # 每周期频次
        total_days = instance.cycle_times  # 总天数
        begin_option = instance.default_beginning_time  # 执行时间基准
        base_interval = instance.base_interval  # 基准间隔

        # 计算开始时间
        start_time = None
        # (0, '无'), (1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')
        from django.utils import timezone
        if begin_option == 1:
            start_time = _add_base_interval(timezone.now(), base_interval)
        elif begin_option == 2:
            start_time = _add_base_interval(first_start_time, base_interval)
        elif begin_option == 3:
            start_time = _add_base_interval(previous_end_time, base_interval)
        elif begin_option == 4:
            start_time = _add_base_interval(timezone.now(), base_interval)  # TODO: 客户出生日期

        if start_time:
            # 计算总次数
            times = total_days // unit_days * cycle_frequency
            # 计算每次间隔小时数
            interval_hours = unit_days * 24 // cycle_frequency
            # 从开始时间开始，每次间隔interval_hours小时，给出时间列表
            schedule_times = []
            from datetime import timedelta
            for i in range(times):
                schedule_times.append(start_time + timedelta(hours=interval_hours * i))

            return schedule_times
        else:
            return []

    schedule = []  # 客户服务日程:[{'customer': customer, 'servicepackage': servicepackage, 'service': service, 'scheduled_time': scheduled_time, 'scheduled_operator': scheduled_operator, 'overtime': overtime}, ]
    first_start_time = None
    previous_end_time = None

    for idx, instance in enumerate(instances):
        schedule_times = _get_schedule_times(
            instance,
            first_start_time,  # 首个服务开始时间
            previous_end_time)  # 上个服务结束时间

        if schedule_times:
            if idx == 0:
                first_start_time = schedule_times[0]  # 获取首个服务开始时间
            previous_end_time = schedule_times[-1]  # 获取上个服务结束时间

        for time in schedule_times:
            print('service:', instance.service, 'scheduled_time:', time)
            schedule.append({
                'scheduled_draft': instance,
                'service': instance.service,  # 服务项目
                'scheduled_time': time,
                'scheduled_operator': instance.scheduled_operator,
                'overtime': instance.overtime,
            })

    return schedule


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
