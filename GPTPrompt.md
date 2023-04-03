# 新增Feature 1, 虚拟职员处理逻辑

## 业务需求
1. 业务要求任务可以指派给某个具体职员或者某个工作小组。
2. 每个职员可以单独承接任务，也可以隶属于某个小组承接指派给小组的任务。
3. 限制条件是，职员仅能接受自己专业角色范围内的服务。

## 业务模型设计&实现
### 1. 引入虚拟职员概念（虚拟职员=某职员或某工作小组）
* 可以承担一项具体任务的具体职员或工作小组。
* 工作小组包含若干具体职员，工作小组和职员是多对多关系。
* 每个职员有若干角色，工作小组的角色是所有成员角色的集合。

### 2. 虚拟职员和职员、工作小组的数据一致性逻辑
* 增删改职员和工作小组的实例时自动维护虚拟职员相应数据
* 虚拟职员的label来自职员或工作小组的label

### 3. 虚拟职员数据结构和逻辑的Django实现

```python
# Hssc基类
class HsscBase(models.Model):
    label = models.CharField(max_length=255, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")
    hssc_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="hsscID")

    class Meta:
        abstract = True

# 职员数据结构定义
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
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="隶属机构")
    wecom_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="企业微信id")

    def save(self, *args, **kwargs):
        super(Staff, self).save(*args, **kwargs)
        VirtualStaff.objects.get_or_create(staff=self)
    
    def delete(self, *args, **kwargs):
        virtual_staff = VirtualStaff.objects.filter(staff=self)
        virtual_staff.delete()
        super(Staff, self).delete(*args, **kwargs)

# 工作小组数据结构定义
class Workgroup(HsscBase):
    leader = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='workgroup_customer', null=True, verbose_name='组长')
    members = models.ManyToManyField(Staff, related_name='workgroup_members', blank=True, verbose_name='组员')

    def save(self, *args, **kwargs):
        super(Workgroup, self).save(*args, **kwargs)
        VirtualStaff.objects.get_or_create(workgroup=self, is_workgroup=True)
    
    def delete(self, *args, **kwargs):
        virtual_staff = VirtualStaff.objects.filter(workgroup=self)
        virtual_staff.delete()
        super(Workgroup, self).delete(*args, **kwargs)

# 虚拟职员数据结构定义：
class VirtualStaff(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, blank=True, null=True, verbose_name='职员')
    workgroup = models.OneToOneField(Workgroup, on_delete=models.CASCADE, blank=True, null=True, verbose_name='工作小组')
    is_workgroup = models.BooleanField(default=False, verbose_name='是否为工作小组')

    def clean(self):
        if not (self.staff or self.workgroup):
            raise ValidationError('一个虚拟职员实例必须关联一个职员或工作小组。')
        if self.staff and self.workgroup:
            raise ValidationError('一个虚拟职员实例不能同时关联职员和工作小组。')

    def save(self, *args, **kwargs):
        self.clean()
        super(VirtualStaff, self).save(*args, **kwargs)

```

### 4. 添加优先操作员(priority_operator)字段
1. 修改Customer.charge_staff外键为VirtualStaff
2. 在以下三个Model中添加priority_operator字段，外键为VirtualStaff
* 作业进程表 OperationProc
* 服务项目安排 CustomerScheduleDraft
* 客户服务日程 CustomerSchedule

### 5. 在业务逻辑中使用priority_operator
1. 从CustomerScheduleDraft --> CustomerSchedule
2. 从CustomerSchedule --> OperationProc 
3. 创建服务进程实例create_service_proc()增加参数priority_operator
4. task.check_proc_awaiting_timeout()中从计划生成服务进程增加参数priority_operator
5. 修改create_service_proc()中的charge_staff处理逻辑
6. 修改dispatch_operator()中的charge_staff处理逻辑
7. 修改get_customer_profile()中的charge_staff处理逻辑
8. 修改update_unassigned_procs()的操作员能看到的未分配服务进程集合——“任务能见逻辑”：
* 服务作业进程的状态为0（未分配）；
* 服务作业进程的操作员为空；
* priority_operator为空或者当前操作员隶属于priority_operator，操作员可能隶属于多个工作小组；

### 6、设计系统变更
1. 在formdesign.define_backup的script_file_header.py文件中添加hssc.service的models.py和admin.py的变更内容
2. 在formdesign.define_operand.models中添加CoreModel，让其记录的增删改与“关联字段基础表”同步。
3. 在其中添加一条记录，名称=虚拟职员，model_name=VirtualStaff。

### 7、测试用例准备
1. 在formdesign管理界面“关联字段”添加“测试责任人”字段，关联内容：虚拟职员
2. 在formdesign管理界面“业务表单-个人基本信息”中添加“测试责任人”字段
3. 在init_core_data.py中增加工作小组测试数据

## 测试
1. 设计系统生产环境生成脚本，备份设计数据，下载设计数据到设计系统开发环境；
2. hssc导入脚本和数据；
3. 业务系统测试。

## 部署
1. 设计系统生产环境生成脚本，备份设计数据，下载设计数据到设计系统开发环境；
2. 清理Buessiness.api_fields='null'和'[]'的数据；
3. 重新备份设计数据和生成脚本；


# 新增Feature 2, 创建诊疗服务进程时判断父进程服务类型，如果是管理调度服务，则尝试拷贝父进程的引用进程表单内容
1. 判断父进程content_object类型是否为CustomerSchedule
2. 如果是，则尝试从reference_operation中逐一拷贝父进程的引用进程表单对象的字段内容

