from django.forms.models import model_to_dict
from core.hsscbase_class import FieldsType
from service.models import *
# 创建服务表单实例
def create_form_instance(operation_proc):
    # 1. 创建空表单
    model_name = operation_proc.service.name.capitalize()
    form_instance = eval(model_name).objects.create(
        customer=operation_proc.customer,
        creater=operation_proc.operator,
        pid=operation_proc,
        cpid=operation_proc.contract_service_proc,
    )
    print('From service.models.create_form_instance, 创建表单实例:', model_name, form_instance, model_to_dict(form_instance))

    # 2. 如果不是基本信息表作业(作业服务表单!=作业服务的实体基本信息表单)，则为属性表，填入表头字段
    service = operation_proc.service
    if service.buessiness_forms.all().first() != service.managed_entity.base_form:
        # 判断当前实体，填入实体基本信息表头字段
        # 通用代码里customer应改为entity
        base_info = eval(service.managed_entity.base_form.service_set.all().first().name.capitalize()).objects.filter(customer=operation_proc.customer).first()
        # *********以下应为生成代码！************
        form_instance.characterfield_family_address = base_info.characterfield_family_address
        form_instance.characterfield_contact_number = base_info.characterfield_contact_number
        form_instance.characterfield_name = base_info.characterfield_name
        form_instance.relatedfield_gender = base_info.relatedfield_gender
        form_instance.datetimefield_date_of_birth = base_info.datetimefield_date_of_birth
        form_instance.save()
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

    form = create_form_instance(new_proc)
    # 更新OperationProc服务进程的form实例信息
    new_proc.object_id = form.id
    new_proc.entry = f'/clinic/service/{new_proc.service.name.lower()}/{form.id}/change'
    new_proc.save()

    return new_proc


# 创建客户服务日志：把服务表单内容写入客户服务日志
def create_customer_service_log(post_data, form_instance):
    from enum import Enum
    from core.models import CustomerServiceLog
    from django.core.exceptions import ObjectDoesNotExist
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


# KMP算法：查找字段名在表达式（字符串）中的位置，并用字段值替换
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
