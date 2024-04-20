from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

import copy
import json

from core.models import HsscFormModel, ServicePackageDetail, TaskProc, OperationProc, Service, L1Service, RecommendedService, CustomerServiceLog, ManagedEntity, Customer
from core.hsscbase_class import FieldsType
from service.models import *

# 从前道表单复制数据到后道表单
def copy_previous_form_data(form, previous_form_data, is_list):
    def _get_parent_form(form):
        """Get the parent form of the given form."""
        if form.pid.parent_proc:
            return form.pid.parent_proc.content_object
        return None    

    def _copy_fields_data(new_form, previous_form_data, copy_fields_name, copy_fields_name_m2m):
        # 向当前表单写入可拷贝的字段内容
        for field_name in copy_fields_name:
            field_value = previous_form_data.get(field_name)
            if field_value:
                setattr(new_form, field_name, field_value)
        new_form.save()

        # 向当前表单写入可拷贝的多对多字段内容
        for field_name in copy_fields_name_m2m:
            m2m_objs = previous_form_data.get(field_name)
            if m2m_objs and isinstance(m2m_objs, QuerySet):
                getattr(new_form, field_name).add(*m2m_objs)

    def _copy_dict_data(form, previous_form_data):
        # 获取父进程表单
        previous_form = _get_parent_form(form)

        if previous_form:
            # 获取表单可拷贝的字段名
            base_fields_name = {field.name for field in HsscFormModel._meta.fields}  # 表单基础字段集合
            base_fields_name.add('id')
            previous_form_fields_name = set(previous_form_data.keys()) - base_fields_name
            form_fields_name = {field.name for field in form._meta.fields} - base_fields_name
            copy_fields_name = previous_form_fields_name.intersection(form_fields_name)
            # 获取表单可拷贝的多对多字段名
            previous_form_fields_name_m2m = {field.name for field in previous_form._meta.many_to_many}
            form_fields_name_m2m = {field.name for field in form._meta.many_to_many}
            copy_fields_name_m2m = previous_form_fields_name_m2m.intersection(form_fields_name_m2m)

            _copy_fields_data(form, previous_form_data, copy_fields_name, copy_fields_name_m2m)

    def _copy_list_data(form, previous_form_data):
        # 获取父进程表单
        previous_form = _get_parent_form(form)

        if previous_form:
            form_name = form.__class__.__name__
            list_model_name = form_name + '_list'
            field_form_name = form_name.lower()

            # 向主表单写入数据
            # 获取表单可拷贝的字段名
            base_fields_name = {field.name for field in HsscFormModel._meta.fields}  # 表单基础字段集合
            base_fields_name.add('id')
            # 获取主表单可拷贝的字段名
            previous_form_fields_name = set(previous_form_data[0].keys()) - base_fields_name
            form_fields_name = {field.name for field in form._meta.fields} - base_fields_name
            copy_fields_name = previous_form_fields_name.intersection(form_fields_name)

            # 获取主表单可拷贝的多对多字段名
            previous_form_fields_name_m2m = {field.name for field in previous_form._meta.many_to_many}
            form_fields_name_m2m = {field.name for field in form._meta.many_to_many}
            copy_fields_name_m2m = previous_form_fields_name_m2m.intersection(form_fields_name_m2m)

            _copy_fields_data(form, previous_form_data[0], copy_fields_name, copy_fields_name_m2m)

            # 向明细表单写入数据
            create_string = f'{list_model_name}.objects.create({field_form_name}=form)'
            for item in previous_form_data:
                # 创建明细表单明细项
                form_instance = eval(create_string)

                # 获取明细表单可拷贝的字段名
                previous_form_fields_name = set(item.keys()) - {'id', 'DELETE'}
                form_fields_name = {field.name for field in form_instance._meta.fields}
                copy_fields_name = previous_form_fields_name.intersection(form_fields_name)
                # 获取明细表单可拷贝的多对多字段名
                previous_form_fields_name_m2m = {field.name for field in previous_form._meta.many_to_many}
                form_fields_name_m2m = {field.name for field in form_instance._meta.many_to_many}
                copy_fields_name_m2m = previous_form_fields_name_m2m.intersection(form_fields_name_m2m)
            
                _copy_fields_data(form_instance, item, copy_fields_name, copy_fields_name_m2m)

    # 根据“分组”标识分别处理copy previous_form_data
    if is_list:
        _copy_list_data(form, previous_form_data)
    else:
        _copy_dict_data(form, previous_form_data)

    return form

def procs_to_forms(procs):  # What is the return type should be? <REFACT-TAG 10> 
    # 1. 获取所有服务进程的表单数据
    forms_data = []
    for proc in procs:
        form_obj = proc.content_object
        # form_obj转换为form_data类型
        form_data = {field.name: getattr(form_obj, field.name) for field in form_obj._meta.fields}
        forms_data.append(form_data)
    return forms_data

# 创建服务表单实例
def create_form_instance(operation_proc, passing_data, form_data, apply_to_group, coroutine_result):
    # 1. 创建空表单
    model_name = operation_proc.service.name.capitalize()
    form_instance = eval(model_name).objects.create(
        customer=operation_proc.customer,
        creater=operation_proc.operator,
        pid=operation_proc,
        cpid=operation_proc.contract_service_proc,
    )

    # 2. 如果QuerySet passing_data不为空, 获取相应的服务表单实例列表 history_forms
    history_forms = []  # <REFACT-TAG 00>
    if passing_data:
        pass
        # history_forms = get_history_forms(operation_proc, passing_data)



    # 3. 如果QuerySet passing_data不为空, copy父进程表单数据
    if passing_data :  # <REFACTED 4>
        if coroutine_result:
            print('*********协程进程，复制协程表单数据*********')
            form_objs = coroutine_result.get_form_objs()
            forms_data = []
            for form_obj in form_objs:
                _fields_data = {field.name: getattr(form_obj, field.name) for field in form_obj._meta.fields}
                _m2m_fields_data = {field.name: getattr(form_obj, field.name).all() for field in form_obj._meta.many_to_many}
                _form_data = {**_fields_data, **_m2m_fields_data}

                form_list_data = []
                # 判断是否存在明细表
                if form_obj._meta.related_objects:
                    related_name = form_obj._meta.related_objects[0].get_accessor_name()
                    form_list_objs = getattr(form_obj, related_name).all()
                    if form_list_objs.exists():
                        for obj in form_list_objs:
                            _fields_data = {field.name: getattr(obj, field.name) for field in obj._meta.fields}
                            _m2m_fields_data = {field.name: getattr(obj, field.name).all() for field in obj._meta.many_to_many}
                            form_list_data.append({**_fields_data, **_m2m_fields_data})
                if form_list_data:
                    form_data = [{**_form_data, **item} for item in form_list_data if item]
                else:
                    form_data = [_form_data]
                forms_data.extend(form_data)
            print('forms_data:', forms_data)
            copy_previous_form_data(form_instance, forms_data, True)
        else:
            # 父进程服务类型为诊疗服务（service_type=2）时，直接copy父进程表单数据
            if operation_proc.service.service_type==2 and form_data:
                copy_previous_form_data(form_instance, form_data, apply_to_group)
            # 父进程服务类型为管理调度服务（service_type=1）时，且父进程content_object类型为CustomerSchedule时，
            # 尝试从content_object.reference_operation中逐一拷贝父进程的引用进程表单对象的字段内容
            elif operation_proc.service.service_type==1 and operation_proc.content_object.__class__.__name__=='CustomerSchedule':
                for proc in operation_proc.content_object.reference_operation:
                    form_obj = proc.content_object
                    # form_obj转换为form_data类型
                    form_data = {field.name: getattr(form_obj, field.name) for field in form_obj._meta.fields}
                    copy_previous_form_data(form_instance, form_data, apply_to_group)

    return form_instance


# 创建新的安排服务包进程
def create_service_package_schedule_instance(proc):
    # 1. 创建客户服务包和服务项目安排: CustomerSchedulePackage, CustomerScheduleDraft
    # 获取服务包信息: ServicePackage, ServicePackageDetail
    servicepackage = proc.service.arrange_service_package
    servicepackagedetails = ServicePackageDetail.objects.filter(servicepackage=servicepackage)
    # 创建客户服务包
    customerschedulepackage = CustomerSchedulePackage.objects.create(
        customer=proc.customer,  # 客户
        operator=proc.creater,  # 作业人员
        creater=proc.creater,  # 创建者
        pid=proc,  # 服务作业进程
        cpid=None,
        servicepackage=servicepackage,  # 服务包
    )
    # 创建服务项目安排
    for servicepackagedetail in servicepackagedetails:
        CustomerScheduleDraft.objects.create(
            schedule_package=customerschedulepackage,  # 客户服务包
            service=servicepackagedetail.service,  # 服务项目
            cycle_unit=servicepackagedetail.cycle_unit,  # 周期单位
            cycle_frequency=servicepackagedetail.cycle_frequency,  # 每周期频次
            cycle_times=servicepackagedetail.cycle_times,  # 周期总数/天数
            default_beginning_time=servicepackagedetail.default_beginning_time,  # 执行时间基准
            base_interval=servicepackagedetail.base_interval,  # 基准间隔
        )
    return customerschedulepackage


# 创建服务进程实例
def create_service_proc(**kwargs):
    # 检查父进程(诊疗类服务)表单是否携带进程控制信息(检查api_fields字段)，如果有，整合所有表单的进程控制信息(charge_staff, operator, scheduled_time)
    # 提取进程控制信息，更新相应控制项内容。Api_field = [('charge_staff', '责任人'), ('operator', '作业人员'), ('scheduled_time', '计划执行时间')]
    try:
        form_data = kwargs['form_data']
        if type(kwargs['form_data']) == dict:
            form_item = form_data
        else:
            form_item = form_data[0]
        # if kwargs['parent_proc'] and kwargs['parent_proc'].service.service_type==2 and kwargs['passing_data'] in [1, 2]:
        if kwargs['parent_proc'] and kwargs['parent_proc'].service.service_type==2 and kwargs['passing_data']:  # <REFACTED 2>
            # 获取父进程表单的api_fields中的进程控制信息：作业人员，计划执行时间，责任人
            api_fields = kwargs['parent_proc'].service.buessiness_forms.all()[0].api_fields
            for system_field, form_field in api_fields.items():
                field_value = form_item.get(form_field['field_name'], None)
                if field_value and system_field == 'hssc_operator':  # operator: 作业人员                    
                    if isinstance(form_item.get(form_field['field_name']), Staff):
                        operator = form_item.get(form_field['field_name']).customer
                        print('operator:', kwargs['operator'])
                        kwargs['operator'] = operator
                        print('operator:', kwargs['operator'])
                elif field_value and system_field == 'hssc_scheduled_time':  # scheduled_time: 计划执行时间
                    scheduled_time = form_item.get(form_field['field_name'])
                    kwargs['scheduled_time'] = scheduled_time
                elif field_value and system_field=='hssc_charge_staff':  # charge_staff: 责任人
                    kwargs['customer'].charge_staff = form_item.get(form_field['field_name'])
                    kwargs['customer'].save()
                else:
                    pass
    except KeyError as e:
        print(f"Missing key in kwargs: {e}")
    except AttributeError as e:
        print(f"Attribute error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    # 创建新的服务作业进程
    params = {
        'service': kwargs['service'],
        'customer': kwargs['customer'],
        'creater': kwargs['creater'],
        'operator': kwargs['operator'],
        'priority_operator': kwargs['priority_operator'],
        'state': kwargs['state'],
        'scheduled_time': kwargs['scheduled_time'],
        'contract_service_proc': kwargs.get('contract_service_proc', None),
        'content_type': kwargs['content_type'],
        'overtime': kwargs['service'].overtime,  # 超时时间
        'working_hours': kwargs['service'].working_hours,  # 工作时间
        'coroutine': kwargs.get('coroutine', None),  # 协程进程
    }

    parent_proc = kwargs.get('parent_proc', None)
    if parent_proc:
        params['parent_proc'] = parent_proc

    new_proc = OperationProc.objects.create(**params)

    # Here postsave signal in service.models
    # 更新允许作业岗位
    role = kwargs['service'].role.all()
    new_proc.role.set(role)

    if new_proc.service.service_type == 1:  # 创建管理调度服务表单进程
        customerschedulepackage = create_service_package_schedule_instance(new_proc)
        new_proc.object_id = customerschedulepackage.id
        new_proc.entry = f'/clinic/service/customerschedulepackage/{customerschedulepackage.id}/change'
        
    else: # 创建诊疗服务表单进程
        form = create_form_instance(new_proc, kwargs['passing_data'], form_data, kwargs['apply_to_group'], kwargs['coroutine_result'])  # <REFACTED 3> -> 不需修改
        # 更新OperationProc服务进程的form实例信息
        new_proc.object_id = form.id
        new_proc.entry = f'/clinic/service/{new_proc.service.name.lower()}/{form.id}/change'
    
    # 解析服务任务进程
    # 1. 如果当前作业是某任务的起始作业，创建新任务进程，作为新作业进程的任务进程
    # 2. 否则，使用父作业进程的任务进程
    try:
        # try to get start_service from L1Service
        l1_service = L1Service.objects.get(start_service=params['service'])
        task_proc = TaskProc.objects.create(
            label=l1_service.label+str(timezone.now().timestamp()),
            l1_service=l1_service,
            state=params['service'],
            operator=params['operator'],
            customer=params['customer'],
        )
    except ObjectDoesNotExist:
        task_proc = parent_proc.task_proc if parent_proc else None
        if task_proc:
            # 更新任务进程的状态
            task_proc.state = params['service']
            task_proc.save()
    # 更新作业进程的任务进程
    new_proc.task_proc = task_proc

    # 保存作业进程
    new_proc.save()

    return new_proc


# 维护推荐服务队列, 删除年龄大于2的推荐条目
def manage_recommended_service(customer):
    # 1. 当前客户的所有推荐服务条目的年龄加1
    RecommendedService.objects.filter(customer=customer).update(age=F('age')+1)
    # 2. 然后删除年龄大于3的条目
    RecommendedService.objects.filter(customer=customer, age__gt=3).delete()


# 根据dict字段类型做字段值的格式转换
def trans_form_to_dict(form_item, form_name):
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
            elif app_label == 'core':
                val_iterator = [id_list.label]  # 适配core.Service
            elif app_label == 'entities':
                val_iterator = [id_list.label]  # 适配core.Medicine
            else:
                val_iterator = [id_list.name]  # 适配entities.Stuff
        return f'{set(val_iterator)}'

    # 预处理--删除键：'id','DELETE', form_name
    form_data = copy.copy(form_item)
    form_data.pop('id', None)
    form_data.pop('DELETE', None)
    form_data.pop(form_name, None)

    for field_name, field_val in form_data.items():
        # 根据字段类型做字段值的格式转换
        field_type = eval(f'FieldsType.{field_name}').value
        if field_type == 'Datetime' or field_type == 'Date' or field_type == 'Boolean':  # 日期/布尔类型暂时不处理
            form_data[field_name] = f'{field_val}'
        elif field_type == 'Numbers' or field_type == 'Decimal':  # 如果字段类型是Numbers或Decimal，直接使用字符串数值
            form_data[field_name] = str(field_val)
        elif field_type == 'String':  # 如果字段类型是String，转换为集合字符串
            form_data[field_name] = str({field_val}) if field_val and field_val!=[''] else '{}'
        else:  # 如果字段类型是关联字段，转换为集合字符串
            form_data[field_name] = _get_set_value(field_type, field_val) if field_val and field_val!=['']  else '{}'
    return form_data


# 创建客户服务日志：把服务表单内容写入客户服务日志
def create_customer_service_log(form, form_set, form_instance):
    form_name = form_instance.__class__.__name__.lower()
    log_data = trans_form_to_dict(form, form_name)
    if form_set:
        formset_copy = copy.deepcopy(form_set)
        form_set_data = []
        # 预处理后的formset data添加到本次服务作业记录中
        # 预处理清理空dict
        for item in formset_copy:
            if item:
                dict_data = trans_form_to_dict(item, form_name)
                form_set_data.append(dict_data)
        log_data[f'{form_name}_list'] = form_set_data

    # 从form_instance.pid.service.buessiness_form中获取form_class
    query_set = form_instance.pid.service.buessiness_forms.all()
    if query_set:
        form_class = query_set[0].form_class
    else:
        form_class = None  # Or some other default value

    # 保存form_data
    try:
        log = CustomerServiceLog.objects.get(pid = form_instance.pid)
        log.data = log_data
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
            form_class=form_class,
            data=log_data,
        )
    return log


# 获取客户基本信息
def get_customer_profile(customer):
    from service.forms import Ju_min_ji_ben_xin_xi_diao_cha_HeaderForm
    # 获取客户的基本信息表单
    base_form = ManagedEntity.objects.get(name='customer').base_form
    base_form_service_name = base_form.service_set.all().first().name
    instance = eval(f'{base_form_service_name.capitalize()}.objects.filter(customer=customer).last()')
    header_form = eval(f'{base_form_service_name.capitalize()}_HeaderForm(instance=instance)')
    url = f'/clinic/service/{base_form_service_name}/{instance.id}/change'
    profile = {
        'id': customer.id,
        'charge_staff': instance.customer.charge_staff.label if instance.customer.charge_staff else '',
        'url': url,
        'form': header_form,
    }

    return profile


# 为新服务分配操作员，返回操作员(Customer类型)
def dispatch_operator(customer, service, current_operator, scheduled_time, task_proc):

    # 0. 当前任务进程的操作员具有新增服务岗位权限, 返回当前任务进程的操作员
    if task_proc and task_proc.operator and set(task_proc.operator.staff.role.all()).intersection(set(service.role.all())):
        return task_proc.operator

    # 1. 当前客户如有责任人，且该责任人是具体职员而非工作小组，且该职员具有新增服务岗位权限，则返回该职员的Customer对象
    charge_staff = customer.charge_staff
    if charge_staff:
        if charge_staff.staff:  # 责任人是具体职员
            # 检查责任人的角色与服务所需角色是否有交集，以确定责任人是否具备岗位权限
            if set(charge_staff.staff.role.all()).intersection(set(service.role.all())):
                return charge_staff.staff.customer
    
    if current_operator.user.is_staff:  # 当前操作员是具体职员
        # 2. 如当前作业员具有新增服务岗位权限，且scheduled_time为当天，则开单给当前作业员
        if set(current_operator.staff.role.all()).intersection(set(service.role.all())) and scheduled_time.date()==timezone.now().date():
            return current_operator

    # 否则，操作员为空，进入共享队列
    return None


# 发送channel_message
def send_channel_message(group_name, message):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, message)


# 搜索给定关键字的客户基本信息列表
def search_customer_profile_list(search_text):
    # 获取客户基本信息表model，系统API字段和展示表头，用于后续查询
    customer_entity = ManagedEntity.objects.get(name='customer')
    customer_profile_model = customer_entity.base_form.service_set.all()[0].name.capitalize()
    api_fields_map = customer_entity.base_form.api_fields

    # 使用姓名字段进行模糊查询
    hssc_name_field = api_fields_map.get('hssc_name', None).get('field_name')
    profiles = eval(f'{customer_profile_model}.objects.filter({hssc_name_field}__icontains="{search_text}")')

    customer_profiles = []
    customer_profile_fields = json.loads(customer_entity.header_fields_json)

    for profile in profiles:
        selected_profile = []
        for field in customer_profile_fields:
            selected_profile.append(getattr(profile, field['name']))

        # 构造客户基本信息列表
        customer_profile = {'customer_id': profile.customer.id, 'selected_profile': selected_profile}
        customer_profiles.append(customer_profile)

    # 构造客户基本信息表头
    customer_profile_fields_header = []
    for field in customer_profile_fields:
        customer_profile_fields_header.append(field['label'])

    # 返回客户基本信息列表和表头
    return customer_profiles, customer_profile_fields_header


def get_customer_profile_field_value(customer, field_name):
    # 获取客户基本信息表model和系统API字段，用于查询hssc_customer_number和hssc_name
    customer_entity = ManagedEntity.objects.get(name='customer')
    customer_profile_model = customer_entity.base_form.service_set.all()[0].name.capitalize()
    api_fields_map = customer_entity.base_form.api_fields
    hssc_field = api_fields_map.get(field_name, None).get('field_name')

    profile = eval(customer_profile_model).objects.filter(customer=customer).last()

    if profile:
        return getattr(profile, hssc_field)
    else:
        return ''

# 更新操作员可见的未分配的服务作业进程
def update_unassigned_procs(operator):
    # 业务逻辑：
    # 先筛选出可行的作业进程available_operation_proc：
    # 1. 服务作业进程的状态为0（未分配）；
    # 2. 服务作业进程的操作员为空；
    # 3. priority_operator为空或者当前操作员隶属于priority_operator；

    # 有权限操作的服务id列表
    allowed_services = [
        service
        for service in Service.objects.filter(service_type__in=[1,2]) 
        if set(service.role.all()).intersection(set(operator.staff.role.all()))
    ]
    allowed_operation_proc = OperationProc.objects.filter(
        operator__isnull=True,  # 操作员为空
        state__in=[0, 3],  # 状态为0（未分配）或3（挂起）
        service__in=allowed_services, # 服务作业进程的服务在allowed_services中
    )

    available_operation_proc = allowed_operation_proc.filter(
        Q(priority_operator__isnull=True) |  # 优先操作员为空
        Q(priority_operator__is_workgroup=True, priority_operator__workgroup__members__in=[operator.staff])  # 当前操作员隶属于优先操作小组
        # Q(priority_operator__is_workgroup=False, priority_operator__staff__customer=operator) |  # 当前操作员即是Staff.customer
    )

    # 根据日期过滤出共享服务（今日待处理服务），过期任务，近期任务(本周待处理服务）
    today = timezone.now().date()
    layout_items = [
        {'title': '共享服务', 'unassigned_procs': available_operation_proc.filter(scheduled_time__date=today)},
        {'title': '过期服务', 'unassigned_procs': available_operation_proc.filter(scheduled_time__date__lt=today)},
        # {'title': '近期任务', 'unassigned_procs': available_operation_proc.filter(scheduled_time__date__gt=today, scheduled_time__date__lt=today+datetime.timedelta(days=7))},
    ]

    # 构造channel_message items
    items = []
    for item in layout_items:
        unassigned_procs = []
        for proc in item['unassigned_procs']:
            hssc_customer_number = get_customer_profile_field_value(proc.customer, 'hssc_customer_number')
            hssc_name = get_customer_profile_field_value(proc.customer, 'hssc_name')
            unassigned_procs.append({
                'id': proc.id,
                'service_id': proc.service.id,
                'service_label': proc.service.label,
                'username': proc.customer.user.username,
                'customer_number': hssc_customer_number,
                'customer_name': hssc_name,
                'charge_staff': proc.customer.charge_staff.label if proc.customer.charge_staff else '',
                'acceptance_timeout': proc.acceptance_timeout,
                'scheduled_time': proc.scheduled_time.strftime("%y.%m.%d %H:%M"),
                'state': proc.state,
            })
        items.append({'title': item['title'], 'unassigned_procs': unassigned_procs})

    # 发送channel_message给操作员
    send_channel_message('unassigned_procs', {'type': 'send_unassigned_procs', 'data': items})


# 更新工作台职员任务列表
def update_staff_todo_list(operator):
    # 根据operator过滤出操作员的今日安排、紧要安排、本周安排
    layout_items = [
        {'title': '今日服务安排', 'todos': OperationProc.objects.staff_todos_today(operator)},
        {'title': '紧要服务安排', 'todos': OperationProc.objects.staff_todos_urgent(operator)},
        {'title': '本周服务安排', 'todos': OperationProc.objects.staff_todos_week(operator)},
    ]

    # 构造channel_message items
    items = []
    for item in layout_items:
        todos = []
        for todo in item['todos']:
            hssc_customer_number = get_customer_profile_field_value(todo.customer, 'hssc_customer_number')
            hssc_name = get_customer_profile_field_value(todo.customer, 'hssc_name')
            todos.append({
                'id': todo.id,
                'customer_id': todo.customer.id,
                'username': todo.customer.user.username,
                'customer_number': hssc_customer_number,
                'customer_name': hssc_name,
                'service_label': todo.service.label,
                'service_id': todo.service.id,
                'customer_phone': todo.customer.phone,
                'customer_address': todo.customer.address,
                'completion_timeout': todo.completion_timeout,
                'scheduled_time': todo.scheduled_time.strftime("%m.%d %H:%M"),
                'state': todo.state,
            })
        items.append({'title': item['title'], 'todos': todos})
    # 发送channel_message给操作员
    send_channel_message(operator.hssc_id, {'type': 'send_staff_todo_list', 'data': items})


# 更新客户服务列表
def update_customer_services_list(customer, history_days=0, history_service_name=''):
    # 判断服务表单是否已经完成，已完成返回空字符串''，否则返回'*'
    def is_service_form_completed(proc):
        content_object = proc.content_object
        # 表单所有字段
        content_object_fields = [field.name for field in content_object._meta.get_fields()]

        # 表单基类字段
        base_class_fields = [field.name for field in HsscFormModel._meta.get_fields()]

        # 表单非基类字段
        non_base_class_fields = [field for field in content_object_fields if field not in base_class_fields]
        for field in non_base_class_fields:
            field_value = getattr(content_object, field)
            if field_value is None or field_value == '':
                return '*'

        return ''

    # 已安排服务
    scheduled_services_today = [
        {
            'service_entry': proc.entry,
            'service_label': proc.service.label,
            'service_id': proc.service.id,
            'completion_timeout': proc.completion_timeout,
            'operator_id': proc.operator.id if proc.operator else '0',
            'state': proc.state,
        } for proc in customer.get_scheduled_services('TODAY')
    ]
    scheduled_services_recent = [
        {
            'service_entry': proc.entry,
            'service_label': proc.service.label,
            'service_id': proc.service.id,
            'completion_timeout': proc.completion_timeout,
            'operator_id': proc.operator.id if proc.operator else '0',
            'state': proc.state,
        } for proc in customer.get_scheduled_services('RECENT')
    ]

    # 历史服务
    history_services = []

    # 如果service是安排服务包和安排服务，则获取所安排服务包或服务的label，并添加到service.label后面；否则获取service的label, 并获取服务表单完成标识
    for proc in customer.get_history_services(history_days, history_service_name):
        service_label = proc.service.label
        is_completed = ''

        if proc.service.name == 'CustomerSchedulePackage':
            service_label = service_label + ' -- ' + proc.content_object.servicepackage.label
        elif proc.service.name == 'CustomerSchedule':
            service_label = service_label + ' -- ' + proc.content_object.service.label

            # 获取服务表单完成标识
            is_completed = is_service_form_completed(proc)

        # 构造历史服务列表
        history_services.append({
            'service_entry': proc.entry,
            'service_label': f'{service_label} {is_completed}',
            'service_id': proc.service.id,
        })

    servicesList = {
        'scheduled_services_today': scheduled_services_today,
        'scheduled_services_recent': scheduled_services_recent,
        'history_services': history_services,
    }
    # 发送channel_message给操作员
    send_channel_message(f'customer_services_{customer.id}', {'type': 'send_customer_services_list', 'data': servicesList})


# 更新客户推荐服务项目列表
def update_customer_recommended_services_list(customer):
    # # 推荐服务
    recommend_services = RecommendedService.objects.filter(customer=customer)
    recommendedServices = [
        {
            'id': recommend_service.id,
            'customer_id': customer.id,
            'service_id': recommend_service.service.id,
            'service_label': recommend_service.service.label,
            'enable_queue_counter': recommend_service.service.enable_queue_counter,
            'queue_count': OperationProc.objects.get_service_queue_count(recommend_service.service),
            'counter': recommend_service.counter,
        } for recommend_service in recommend_services if recommend_service.service is not None
    ]

    # 发送channel_message给操作员
    send_channel_message(f'customer_recommended_services_{customer.id}', {'type': 'send_customer_recommended_services_list', 'data': recommendedServices})


# 把客户服务计划安排转为客户服务日程安排
def get_services_schedule(instances, customer_start_time):
    def _get_schedule_times(instance, idx, first_start_time, previous_end_time, customer_start_time):
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

        if idx == 0 and begin_option in [2,3]:  # 修正首个服务的开始时间
            begin_option = 0

        # 计算开始时间
        start_time = None
        # (0, '指定开始时间'), (1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')
        if begin_option == 0:
            start_time = customer_start_time
        elif begin_option == 1:
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
            for i in range(times):
                schedule_times.append(start_time + timedelta(hours=interval_hours * i))

            return schedule_times
        else:
            return []

    schedules = []  # 客户服务日程:[{'customer': customer, 'servicepackage': servicepackage, 'service': service, 'scheduled_time': scheduled_time, 'scheduled_operator': scheduled_operator, 'overtime': overtime}, ]
    first_start_time = None
    previous_end_time = None

    for idx, instance in enumerate(instances):
        schedule_times = _get_schedule_times(
            instance,
            idx,  
            first_start_time,  # 首个服务开始时间
            previous_end_time,  # 上个服务结束时间
            customer_start_time, # 用户指定开始时间
        )

        if schedule_times:
            if idx == 0:
                first_start_time = schedule_times[0]  # 获取首个服务开始时间
            previous_end_time = schedule_times[-1]  # 获取上个服务结束时间

        for time in schedule_times:
            schedules.append({
                'scheduled_draft': instance,
                'service': instance.service,  # 服务项目
                'scheduled_time': time,
                'scheduled_operator': instance.scheduled_operator,
                'priority_operator': instance.priority_operator,
                'overtime': instance.overtime,
            })

    return schedules 


# 创建一条客户服务日程
def create_customer_schedule(**kwargs):
    customer = kwargs.get('customer', None)
    operator = kwargs.get('operator', None)
    creater = kwargs.get('creater', None)
    service = kwargs.get('service', None)
    scheduled_time = kwargs.get('scheduled_time', None)
    pid = kwargs.get('pid', None)

    # 生成CustomerScheduleList记录
    schedule_list = CustomerScheduleList.objects.create(
        customer = customer,
        operator = operator,
        creater = creater,
        plan_serial_number = service.label + '--' + pid.created_time.strftime('%Y-%m-%d') + '--' + pid.operator.name,
        service = service,
        is_ready = False
    )

    # 创建客户服务日程对象
    customer_name = get_customer_profile_field_value(customer, 'hssc_name')
    customer_schedule = CustomerSchedule(
        customer_schedule_list = schedule_list,
        customer=customer,
        operator=operator,  # 作业人员
        creater=creater,  # 创建者
        service=service,
        scheduled_time=scheduled_time,
        pid = pid,
        # reference_operation = reference_operation,
        label = f"{service.label}-{customer_name}",
    )
    # 设置其他默认值
    customer_schedule.name = f"{type(customer_schedule).__name__}-{customer_schedule.hssc_id}"
    customer_schedule.save()

    # 更新CustomerScheduleList的is_ready状态，完成一次创建服务计划安排事务
    schedule_list.is_ready = True
    schedule_list.save()

    return customer_schedule


# 估算服务项目的计划执行时间
def eval_scheduled_time(_service, _operator):
    scheduled_time = timezone.now()

    if _operator:  # 若存在operator，返回operator当天的todo队列的队尾时间，
        # 查询当天最后一条服务进程
        last_staff_todo = OperationProc.objects.filter(
            operator=_operator,
            state__in=[0, 1, 2, 3],
            scheduled_time__date=timezone.now().date()
        ).order_by('-scheduled_time').first()

        # 如果存在当天最后一条服务进程，则计算队列时间，否则返回当前时间
        if last_staff_todo:
            if last_staff_todo.service.working_hours:
                scheduled_time = last_staff_todo.scheduled_time + last_staff_todo.service.working_hours
            else:
                scheduled_time = last_staff_todo.scheduled_time

            if scheduled_time < timezone.now():
                scheduled_time = timezone.now()

    else:  # 否则返回当天此服务进程的队列累加时间
        # 查询当天最后一条同服务类型的服务进程
        last_service_proc = OperationProc.objects.filter(
            service=_service,
            state__in=[0, 1, 2, 3],
            scheduled_time__date=timezone.now().date()
        ).order_by('-scheduled_time').first()

        # 如果存在当天最后一条同服务类型的服务进程，则计算队列时间，否则返回当前时间
        if last_service_proc:
            if _service.working_hours:
                scheduled_time = last_service_proc.scheduled_time + _service.working_hours
            else:
                scheduled_time = last_service_proc.scheduled_time

            if scheduled_time < timezone.now():
                scheduled_time = timezone.now()

    return scheduled_time


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
