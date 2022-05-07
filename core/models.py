from django.db import models
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.shortcuts import reverse
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from enum import Enum
from time import time
import datetime

from pypinyin import lazy_pinyin

# 导入自定义作业完成信号
from core.signals import operand_finished
from core.hsscbase_class import HsscBase, HsscPymBase
from icpc.models import *
from dictionaries.models import *


def gen_slug(s):
    slug = slugify(s, allow_unicode=True)
    return slug + f'-{int(time())}'


# 角色表
class Role(HsscPymBase):
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="岗位描述")

    class Meta:
        verbose_name = "业务岗位"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 业务表单定义
class BuessinessForm(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name="表单说明")
    meta_data = models.JSONField(null=True, blank=True, verbose_name="元数据")
    
    class Meta:
        verbose_name = '业务表单'
        verbose_name_plural = verbose_name


# 管理实体定义
class ManagedEntity(HsscPymBase):
    app_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="所属app名")
    model_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="模型名")
    base_form = models.OneToOneField('BuessinessForm', on_delete=models.SET_NULL, null=True, verbose_name="基础表单")

    class Meta:
        verbose_name = "业务管理实体"
        verbose_name_plural = verbose_name


# 作业基础信息表
class Service(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    buessiness_forms = models.ManyToManyField(BuessinessForm, through='BuessinessFormsSetting', verbose_name="作业表单")
    managed_entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, null=True, verbose_name="管理实体")
    Operation_priority = [(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
    is_system_service = models.BooleanField(default=False, verbose_name='系统内置服务')
    role = models.ManyToManyField(Role, blank=True, verbose_name="服务岗位")
    History_services_display=[(0, '所有历史服务'), (1, '当日服务')]
    history_services_display = models.PositiveBigIntegerField(choices=History_services_display, default=0, blank=True, null=True, verbose_name='历史服务默认显示')
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列数量')
    suppliers = models.CharField(max_length=255, blank=True, null=True, verbose_name="供应商")
    not_suitable = models.CharField(max_length=255, blank=True, null=True, verbose_name='不适用对象')
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='完成时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')
    working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
    frequency = models.CharField(max_length=255, blank=True, null=True, verbose_name='频次')
    cost = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='成本')
    load_feedback = models.BooleanField(default=False, verbose_name='是否反馈负荷数量')
    resource_materials = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套物料')
    resource_devices = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套设备')
    resource_knowledge = models.CharField(max_length=255, blank=True, null=True, verbose_name='服务知识')

    class Meta:
        verbose_name = "服务"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

class BuessinessFormsSetting(HsscBase):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="作业")
    buessiness_form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="表单")
    is_list = models.BooleanField(default=False, verbose_name="列表样式")

    class Meta:
        verbose_name = '作业表单设置'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 服务包类型信息表
class ServicePackage(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    services = models.ManyToManyField(Service, through='ServicePackageDetail', verbose_name="服务项目")
    Begin_time_setting = [(0, '人工指定'), (1, '出生日期')]
    begin_time_setting = models.PositiveSmallIntegerField(choices=Begin_time_setting, default=0, verbose_name='开始时间参考')
    duration = models.DurationField(blank=True, null=True, verbose_name="持续周期", help_text='例如：3 days, 22:00:00')
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='执行时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')

    class Meta:
        verbose_name = "服务包"
        verbose_name_plural = verbose_name
        ordering = ['id']

class ServicePackageDetail(HsscPymBase):
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    Cycle_options = [(0, '总共'), (1, '每天'), (2, '每周'), (3, '每月'), (4, '每季'), (5, '每年')]
    cycle_option = models.PositiveSmallIntegerField(choices=Cycle_options, default=0, blank=True, null=True, verbose_name='周期')
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="次数")
    reference_start_tim = models.DurationField(blank=True, null=True, verbose_name="参考起始时间", help_text='例如：3 days, 22:00:00')
    duration = models.DurationField(blank=True, null=True, verbose_name="持续周期", help_text='例如：3 days, 22:00:00')
    check_awaiting_timeout = models.BooleanField(default=False, verbose_name='检查等待超时')

    class Meta:
        verbose_name = "服务内容模板"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.service)


# 系统作业指令表
class SystemOperand(HsscBase):
    func = models.CharField(max_length=255, blank=True, null=True, verbose_name="内部实现函数")
    parameters = models.CharField(max_length=255, blank=True, null=True, verbose_name="参数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="描述")
    Applicable = [(0, '作业'), (1, '单元服务'), (2, '服务包'), (3, '全部')]
    applicable = models.PositiveSmallIntegerField(choices=Applicable, default=1, verbose_name='适用范围')

    class Meta:
        verbose_name = '系统自动作业'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.func

    def execute(self, **kwargs):
        '''
        执行作业
        '''
        class SystemOperandFunc(Enum):
            CREATE_NEXT_SERVICE = self.create_next_service  # 生成后续服务
            RECOMMEND_NEXT_SERVICE = self.recommend_next_service  # 推荐后续服务
            VIOLATION_ALERT = self.alert_content_violations  # 内容违规提示
            SEND_NOTIFICATION = self.send_notification  # 发送提醒

		# 调用OperandFuncMixin中的系统自动作业函数
        return eval(f'SystemOperandFunc.{self.func}')(**kwargs)

    def create_next_service(self, **kwargs):
        '''
        生成后续服务
        '''
        # 准备新的服务作业进程参数
        operation_proc = kwargs['operation_proc']
        customer = operation_proc.customer
        operator = kwargs['operator']
        next_service = kwargs['next_service']
        contract_service_proc = operation_proc.contract_service_proc

        # 创建新的服务作业进程
        new_proc=OperationProc.objects.create(
            service=next_service,  # 服务
            customer=customer,  # 客户
            creater=operator,  # 创建者
            state=0,  # 进程状态
            scheduled_time=datetime.datetime.now(),  # 创建时间
            parent_proc=operation_proc,  # 当前进程是被创建进程的父进程
            contract_service_proc=contract_service_proc,  # 所属合约服务进程
        )
        # Here postsave signal in service.models
        # 更新允许作业岗位
        role = next_service.role.all()
        new_proc.role.set(role)

        return f'创建服务作业进程: {new_proc}'

    def recommend_next_service(self, **kwargs):
        '''
        推荐后续服务
        '''
        # 准备新的服务作业进程参数
        operation_proc = kwargs['operation_proc']
        # 创建新的服务作业进程
        _recommended = RecommendedService.objects.create(
            service=kwargs['next_service'],  # 推荐的服务
            customer=operation_proc.customer,  # 客户
            creater=kwargs['operator'],  # 创建者
            pid=operation_proc,  # 当前进程是被推荐服务的父进程
            cpid=operation_proc.contract_service_proc,  # 所属合约服务进程
        )
        return f'推荐服务作业: {_recommended}'

    def alert_content_violations(self, **kwargs):
        '''
        内容违规提示
        '''
        print('alert_content_violations:', '内容违规提示')
        return '内容违规提示'

    def send_notification(self, **kwargs):
        '''
        发送提醒
        '''
        # 准备服务作业进程参数
        operation_proc = kwargs['operation_proc']

        # 获取提醒人员list
        _reminders_option = kwargs['reminders']
        reminders = _get_reminders(_reminders_option)

        # 创建提醒消息
        for customer in reminders:
            _ = Message.objects.create(
                message=kwargs['message'],  # 消息内容
                customer=customer,  # 客户
                creater=kwargs['operator'],  # 创建者
                pid=operation_proc,  # 当前进程是被推荐服务的父进程
                cpid=operation_proc.contract_service_proc,  # 所属合约服务进程
            )

        def _get_reminders(_option):
            '''
            用选项值为list.index获取提醒对象列表
            '''
            reminder_option = [
                operation_proc.customer,  # 0: 发送给当前客户
                kwargs['operator'],  # 1: 发送给当前作业人员
                # return workgroup_list,  # 2: 发送给当前作业组成员
            ]
            return [reminder_option[_option]]

        return f'生成提醒消息OK'


# 事件规则表
from core.utils import keyword_replace
from core.hsscbase_class import FieldsType
class EventRule(HsscBase):
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name="表达式")
    Detection_scope = [(0, '所有历史表单'), (1, '本次服务表单'), (2, '单元服务表单')]
    detection_scope = models.PositiveSmallIntegerField(choices=Detection_scope, default=1, blank=True, null=True, verbose_name='检测范围')
    weight = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="权重")
    expression = models.TextField(max_length=1024, blank=True, null=True, verbose_name="内部表达式")
    expression_fields = models.CharField(max_length=1024, blank=True, null=True, verbose_name="内部表达式字段")

    class Meta:
        verbose_name = '条件事件'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def is_satified(self, form_data):
        '''
        检查表达式是否满足
        parameters: form_data
        return: Boolean
		'''

        # 完成事件直接返回
        if self.expression == 'completed':
            return True
        else:
            print('From EventRule.is_satified 检查表达式:', self.expression, )
            print('检查字段:', self.expression_fields)
            # 构造一个字段字典，存储表达式内的字段及它们的值
            expression_fields = {}
            # 预处理 self.expression_fields: 去除空格，以逗号转为数组，再转为集合
            expression_fields_set = set(self.expression_fields.strip().split(','))
            # 获取需要被检查的表达式包含的字段名称, 转换为数组
            for field_name in expression_fields_set:
                _type = eval(f'FieldsType.{field_name}').value
                if _type == 'Numbers':  # 如果字段类型是Numbers，直接转换为字符串
                    expression_fields[field_name] = f'{form_data[field_name]}'
                elif _type == 'String':  # 如果字段类型是String，转换为集合字符串
                    expression_fields[field_name] = str(set(f'{form_data[field_name]}'.replace(' ', '')))
                elif _type == 'Datetime':
                    pass
                elif _type == 'Date':
                    pass
                else:  # 字段值是关联字典，转换为集合字符串
                    # 转换id列表为字典值列表
                    if form_data.getlist(field_name):  # 如果列表字段值不为空
                        str_value_set = self._convert_id_to_value(_type, form_data.getlist(field_name))
                        expression_fields[field_name] = str(str_value_set)
            return eval(keyword_replace(self.expression, expression_fields))

    @staticmethod
    def _convert_id_to_value(_type, id_list):
        print('进入：', _type, id_list)
        _model_list = _type.split('.')
        app_label = _model_list[0]
        model_name = _model_list[1]
        class ConvertIdToValue(Enum):
            icpc = map(lambda x: eval(model_name).objects.get(id=x).iname, id_list)
            dictionaries = map(lambda x: eval(model_name).objects.get(id=x).value, id_list)
            # medcine = map(lambda x: eval(model_name).objects.get(id=x).name, id_list)
        val_iterator = eval(f'ConvertIdToValue.{app_label}').value
        return set(val_iterator)


# 服务规格设置
class ServiceSpec(HsscBase):
    class Meta:
        verbose_name = "服务规格"
        verbose_name_plural = verbose_name
        ordering = ['id']

# 服务规则库
class ServiceRule(HsscBase):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE,  blank=True, null=True, verbose_name='条件事件')
    system_operand = models.ForeignKey(SystemOperand, on_delete=models.CASCADE, blank=True, null=True, verbose_name='系统作业')
    next_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='next_service', verbose_name='后续服务')
    Receive_form = [(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')]  # 接收表单数据
    passing_data = models.PositiveSmallIntegerField(choices=Receive_form, default=0,  blank=True, null=True, verbose_name='接收表单')
    Complete_feedback = [(0, '否'), (1, '返回完成状态'), (2, '返回表单')]
    complete_feedback = models.PositiveSmallIntegerField(choices=Complete_feedback, default=0,  blank=True, null=True, verbose_name='完成反馈')
    Reminders = [(0, '客户'), (1, '服务人员'), (2, '服务小组')]
    reminders = models.PositiveSmallIntegerField(choices=Reminders, default=0,  blank=True, null=True, verbose_name='提醒对象')
    message = models.CharField(max_length=512, blank=True, null=True, verbose_name='消息内容')
    Interval_rule_options = [(0, '等于'), (1, '小于'), (2, '大于')]
    interval_rule = models.PositiveSmallIntegerField(choices=Interval_rule_options, blank=True, null=True, verbose_name='间隔条件')
    interval_time = models.DurationField(blank=True, null=True, verbose_name="间隔时间", help_text='例如：3 days, 22:00:00')
    is_active = models.BooleanField(choices=[(False, '否'), (True, '是')], default=True, verbose_name='启用')
    service_spec = models.ForeignKey(ServiceSpec, on_delete=models.CASCADE, null=True, verbose_name='服务规格')

    class Meta:
        verbose_name = '服务规则'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.service)

@receiver(operand_finished)
def check_rules(sender, **kwargs):
    '''
    服务表单保存后根据服务规则生成业务事件
    params: operation_proc.hssc_id, service.hssc_id
    return: 
    how:
		0. 获取服务作业完成信号
		1. 根据service.hssc_id获取需要检查的service_rule集合
		2. 逐一检查event_rule.expression是否满足
		3. 若满足则构造事件参数，生成自定义信号“发生业务事件”，传给调度函数。事件参数：{}
    '''
    # 用operand_finished信号参数的pid获取operation_proc
    operation_proc = OperationProc.objects.get(id=kwargs['pid'])
    # 用operand_finished信号参数的uid获取操作员的Customer信息
    operator = User.objects.get(id=kwargs['uid']).customer
    # 获取服务表单数据：POST表单数据
    form_data = kwargs['form_data']

    # 根据operation_proc.service.hssc_id获取service_rule集合
    service_rules = ServiceRule.objects.filter(service=operation_proc.service, is_active=True)
    # 逐一检查event_rule.expression是否满足
    print('From check_rules 检查服务规则：', service_rules)
    for service_rule in service_rules:
        # 如果event_rule.expression为真，则构造事件参数，生成业务事件
        if service_rule.event_rule.is_satified(form_data):
            # 构造作业参数
            print('From check_rules 满足规则：', service_rule)
            operation_params = {
                'operation_proc': operation_proc,
                'operator': operator,
                'service': service_rule.service,
                'next_service': service_rule.next_service,
                'passing_data': service_rule.passing_data,
                'complete_feedback': service_rule.complete_feedback,
                'reminders': service_rule.reminders,
                'message': service_rule.message,
                'interval_rule': service_rule.interval_rule,
                'interval_time': service_rule.interval_time,
            }
            # 执行系统自动作业
            print('From check_rules 操作参数:', operation_params)
            _result = service_rule.system_operand.execute(**operation_params)
            print('From check_rules 执行结果:', _result)
    return None


class ContractService(HsscPymBase):
    is_active = models.BooleanField(default=True, verbose_name='启用')
    is_deleted = models.BooleanField(default=False, verbose_name='删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '合约服务'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.label)

# 服务进程表 ServiceProc
class ContractServiceProc(HsscBase):
    contract_service = models.ForeignKey(ContractService, on_delete=models.CASCADE, verbose_name="合约服务")
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='service_proc_customer', verbose_name="客户")  # 客户id: cid
    creater = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='service_proc_creater', verbose_name="创建者")  # 创建者id: cid
    current_service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业状态")
    Operation_priority = [(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name="优先级")

    class Meta:
        verbose_name = "合约服务进程"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.customer.name


#作业进程状态机操作码ocode
class OperationCode(Enum):
	CRE = 0  # CREATE
	CTR = 1  # CREATED TO READY
	RTR = 2  # READY TO RUNNING
	RTH = 3  # RUNNING TO HANGUP
	HTR = 1  # HANGUP TO READY
	RTC = 4  # RUNNING TO COMPLETED


class OperationProcManager(models.Manager):
    def get_unassigned_proc(self, operator):
	# 获取待分配作业进程: 状态为创建，且未分配操作员，服务岗位为操作员所属岗位，以及用户服务小组为操作员所属服务小组
        return self.filter(state=0, operator=None, service__in=Service.objects.filter(role__in=operator.staff.role.all()),)

# 作业进程表 OperationProc
class OperationProc(HsscBase):
    # 作业进程id: pid
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name="服务")  # 作业id: oid
    operator = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_operator', verbose_name="操作员")  # 作业员id: uid
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_customer', verbose_name="客户")  # 客户id: cid
    creater = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_creater', verbose_name="创建者")  # 创建者id: cid
    role = models.ManyToManyField(Role, blank=True, verbose_name="作业岗位")
	# 作业状态: state
    Operation_proc_state = [(0, '创建'), (1, '就绪'), (2, '运行'), (3, '挂起'), (4, '结束')]
    state = models.PositiveSmallIntegerField(choices=Operation_proc_state, verbose_name="作业状态")
    priority = models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name="优先级")
    entry = models.CharField(max_length=250, blank=True, null=True, db_index=True, verbose_name="作业入口")  # 作业入口: /clinic/service/model_name/model_id/change
    parent_proc = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="父进程")  # 父作业进程id: ppid
    contract_service_proc = models.ForeignKey(ContractServiceProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="服务进程")  # 服务进程id: spid
    form_slugs = models.JSONField(blank=True, null=True, verbose_name="表单索引")
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="计划执行时间")
    created_time = models.DateTimeField(editable=False, null=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(editable=False, null=True, verbose_name="修改时间")
    objects = OperationProcManager()

    class Meta:
        verbose_name = "作业进程"
        verbose_name_plural = "作业进程"
        ordering = ['id']

    def __str__(self):
		# return 作业名称-客户姓名
        return "%s - %s - %s" %(self.id, self.service.label, self.creater.name)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_time = timezone.now()
        self.modified_time = timezone.now()
        if not self.name:
            self.name = self.service.label
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # 返回作业入口url
        return self.entry

    def set_operator(self, operator):
        # 设置作业进程操作员
        self.operator = operator
        self.save()

    def update_state(self, ocode):
        '''
        通过作业进程操作码维护作业进程状态：
	    	Operation_proc_state = [(0, '创建'), (1, '就绪'), (2, '运行'), (3, '挂起'), (4, '结束')]
        '''
        self.state = OperationCode[ocode].value
        self.save()


class StaffTodoManager(models.Manager):
	# 当天常规任务
    def today_todos(self, operator):
        today = datetime.date.today()
        return self.filter(
            operator=operator, 
            priority=3,
            scheduled_time__year=int(today.strftime('%Y')),
            scheduled_time__month=int(today.strftime('%m')),
            scheduled_time__day=int(today.strftime('%d')),
            ).exclude(state=4)
        
	
	# 紧要任务安排
    def urgent_todos(self, operator):
        return self.filter(operator=operator, priority__lt=3).exclude(state=4).order_by('priority')

	# 未来七天任务
    def week_todos(self, operator):
        # today = datetime.date.today()
        startTime = datetime.datetime.now() + datetime.timedelta(days=1)
        endTime = datetime.datetime.now() + datetime.timedelta(days=7)
        return self.filter(
            operator=operator, 
            priority=3, 
            # scheduled_time__year=int(today.strftime('%Y')),
            # scheduled_time__week=int(today.strftime('%W')),
            scheduled_time__range=(startTime, endTime),
            ).exclude(state=4)

class StaffTodo(HsscBase):
    operation_proc = models.OneToOneField(OperationProc, on_delete=models.CASCADE, verbose_name="作业进程")
    operator = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="操作员")
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="计划执行时间")
    Operation_proc_state = [(0, '创建'), (1, '就绪'), (2, '运行'), (3, '挂起'), (4, '结束')]
    state = models.PositiveSmallIntegerField(choices=Operation_proc_state, verbose_name="作业状态")
    customer_number = models.CharField(max_length=250, blank=True, null=True, verbose_name="居民档案号")
    customer_name = models.CharField(max_length=250, blank=True, null=True, verbose_name="姓名")
    service_label = models.CharField(max_length=250, blank=True, null=True, verbose_name="服务项目")
    customer_phone = models.CharField(max_length=250, blank=True, null=True, verbose_name="联系电话")
    customer_address = models.CharField(max_length=250, blank=True, null=True, verbose_name="家庭地址")
    priority = models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name="优先级")
    objects = StaffTodoManager()

    class Meta:
        verbose_name = "员工任务清单"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return "%s - %s - %s" %(self.id, self.service_label, self.customer_name)

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = f'{self.customer_name} - {self.service_label}'
        return super().save(*args, **kwargs)

@receiver(post_save, sender=OperationProc)
def sync_proc_todo_list(sender, instance, created, **kwargs):
    # 根据服务进程创建待办事项
    if instance.operator and instance.customer:
        try :
            todo = instance.stafftodo
            todo.scheduled_time = instance.scheduled_time
            todo.state = instance.state
            todo.priority = instance.priority
            todo.save()
        except StaffTodo.DoesNotExist:
            todo = StaffTodo.objects.create(
                operation_proc=instance,
                operator=instance.operator,
                scheduled_time=instance.scheduled_time,
                state=instance.state,
                customer_number=instance.customer.name,
                customer_name=instance.customer.name,
                service_label=instance.service.label,
                customer_phone=instance.customer.phone,
                customer_address=instance.customer.address,
                priority = instance.priority
            )


# 用户基本信息
class Customer(HsscBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='客户')
    name = models.CharField(max_length=50, verbose_name="姓名")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="电话")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="地址")
    charge_staff = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='负责人')
    workgroup = models.ForeignKey('Workgroup', on_delete=models.SET_NULL, blank=True, null=True, related_name='customer_workgroup', verbose_name='服务小组')
    health_record = models.JSONField(blank=True, null=True, verbose_name="健康记录")

    class Meta:
        verbose_name = "客户注册信息"
        verbose_name_plural = "客户注册信息"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = self.name
        super().save(*args, **kwargs)

    def update_health_record(self, health_record):
        '''
        设置健康记录
        '''
        pass

    def get_profile(self) -> 'QuerySet[Customer]':
        '''
        获取客户基本信息
        '''
        return self

    def get_history_services(self) -> 'QuerySet[OperationProc]':
        '''
        获取客户历史服务列表
        '''
        return self.operation_proc_customer.filter(state=4).exclude(service__in=Service.objects.filter(name__in=['Z6201', 'user_login']))

    def get_recommanded_services(self) -> 'QuerySet[RecommendedService]':
        '''
        获取客户推荐服务列表
        '''
        return self.recommendedservice_customer.all()

    def get_scheduled_services(self) -> 'QuerySet[OperationProc]':
        '''
        获取已安排服务列表
        '''
        return self.operation_proc_customer.filter(state__in = [0, 1, 2, 3])


# 职员基本信息
class Staff(HsscBase):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, verbose_name='员工')
    role = models.ManyToManyField(Role, related_name='staff_role', verbose_name='角色')
    email = models.EmailField(max_length=50)
    Title = [(i, i) for i in ['主任医师', '副主任医师', '主治医师', '住院医师', '主任护师', '副主任护师', '主管护师', '护士长', '护士', '其他']]
    title = models.PositiveSmallIntegerField(choices=Title, blank=True, null=True, verbose_name='职称')
    is_assistant_physician = models.BooleanField(blank=True, null=True, verbose_name='助理医师')
    resume = models.TextField(blank=True, null=True, verbose_name='简历')
    Service_Lever = [(i, i) for i in ['低', '中', '高']]
    service_lever = models.PositiveSmallIntegerField(choices=Service_Lever, blank=True, null=True, verbose_name='服务级别')
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='挂号费')
    standardized_workload = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='标化工作量')

    class Meta:
        verbose_name = "员工基本信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = self.customer.label
        if not self.name:
            self.name = self.customer.name
        super().save(*args, **kwargs)


# 工作组
class Workgroup(HsscBase):
    leader = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='workgroup_customer', null=True, verbose_name='组长')
    members = models.ManyToManyField(Staff, related_name='workgroup_members', blank=True, verbose_name='组员')

    class Meta:
        verbose_name = "服务小组"
        verbose_name_plural = "服务小组"
        ordering = ['id']

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)


class HsscFormModel(HsscBase):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='%(class)s_customer', verbose_name="客户")
    operator = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='%(class)s_operator', verbose_name="操作员")
    creater = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='%(class)s_creater', verbose_name="创建者")
    pid = models.OneToOneField(OperationProc, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_pid', verbose_name="作业进程id")
    cpid = models.ForeignKey(ContractServiceProc, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_sid', verbose_name="服务进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")
    created_time = models.DateTimeField(editable=False, null=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(editable=False, null=True, verbose_name="更新时间")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_time = timezone.now()
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        self.updated_time = timezone.now()
        return super().save(*args, **kwargs)

    def get_autocomplete_fields(self):
        autocompelte_fields_name=[]
        for field in self.__class__._meta.get_fields():
            if (field.one_to_one or field.many_to_one):  # 一对一、多对一字段
                autocompelte_fields_name.append(field.name)
        return autocompelte_fields_name

    def get_absolute_url(self):
        return reverse(f'{self.__class__.__name__}_detail_url', kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse(f'{self.__class__.__name__}_update_url', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse(f'{self.__class__.__name__}_delete_url', kwargs={'slug':self.slug})


class RecommendedService(HsscFormModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name="推荐服务")

    class Meta:
        verbose_name = "推荐服务"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.service.label)


class Message(HsscFormModel):
    message = models.CharField(max_length=512, blank=True, null=True, verbose_name="消息")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = "消息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.message)
