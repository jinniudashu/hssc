from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from core.models import Form


# 字段定义
# 字符字段
class CharacterField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="名称")
    label = models.CharField(max_length=100, verbose_name="组件名称", null=True, blank=True)
    Char_Type = [('CharField', '单行文本'), ('TextField', '多行文本')]
    type = models.CharField(max_length=50, choices=Char_Type, default='CharField', verbose_name="类型")
    length = models.PositiveSmallIntegerField(default=255, verbose_name="字符长度")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "字符字段"
        verbose_name_plural = "字符字段"


# 数值字段
class NumberField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="名称")
    label = models.CharField(max_length=100, verbose_name="组件名称", null=True, blank=True)
    Number_Type = [('IntegerField', '整数'), ('DecimalField', '固定精度小数'), ('FloatField', '浮点数')]
    type = models.CharField(max_length=50, choices=Number_Type, default='IntegerField', verbose_name="类型")
    max_digits = models.PositiveSmallIntegerField(default=10, verbose_name="最大位数", null=True, blank=True)
    decimal_places = models.PositiveSmallIntegerField(default=2, verbose_name="小数位数", null=True, blank=True)
    standard_value = models.FloatField(null=True, blank=True, verbose_name="标准值")
    up_limit = models.FloatField(null=True, blank=True, verbose_name="上限")
    down_limit = models.FloatField(null=True, blank=True, verbose_name="下限")
    display_unit = models.BooleanField(default=False, verbose_name="显示单位")
    unit = models.CharField(max_length=50, null=True, blank=True, verbose_name="单位")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "数值字段"
        verbose_name_plural = "数值字段"


# 日期时间字段
class DTField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="名称")
    label = models.CharField(max_length=100, verbose_name="组件名称", null=True, blank=True)
    DT_Type = [('DateField', '日期'), ('DateTimeField', '日期时间')]
    type = models.CharField(max_length=50, choices=DT_Type, default='DateField', verbose_name="类型")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "日期字段"
        verbose_name_plural = "日期字段"


# 选择字段
class ChoiceField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="名称")
    label = models.CharField(max_length=100, verbose_name="组件名称", null=True, blank=True)
    choice_type = [('ChoiceField', '单选'), ('MultipleChoiceField', '多选')]
    type = models.CharField(max_length=50, choices=choice_type, default='ChoiceField', verbose_name="类型")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "选择字段"
        verbose_name_plural = "选择字段"


# 关联字段
class RelatedField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="名称")
    label = models.CharField(max_length=100, verbose_name="组件名称", null=True, blank=True)
    related_type = [('dic', '关联字典'), ('sys', '关联系统表')]
    type = models.CharField(max_length=50, choices=related_type, default='dic', verbose_name="类型")
    related_content = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "关联字段"
        verbose_name_plural = "关联字段"


# 计算字段
class ComputeField(models.Model):
    pass


# 组件定义
class Component(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="名称")
    label = models.CharField(max_length=100, verbose_name="组件名称", null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    attribute = models.JSONField(verbose_name="属性")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "基础组件"
        verbose_name_plural = "基础组件"
        ordering = ['id']


# 基础表单定义
class BaseModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    label = models.CharField(max_length=100, verbose_name="表单名称", null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    components = models.ManyToManyField(Component, verbose_name="组件清单")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "基础表单"
        verbose_name_plural = "基础表单"
        ordering = ['id']


# 基础视图定义
class SubForm(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    label = models.CharField(max_length=100, verbose_name="子表单", null=True, blank=True)
    display_fields = models.TextField(max_length=1024, blank=True, null=True, verbose_name="表单字段")
    FORM_STYLE = [
		('detail', '详情'),
		('list', '列表'),
	]
    style = models.CharField(max_length=50, choices=FORM_STYLE, default='detail', verbose_name='风格')

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "基础视图"
        verbose_name_plural = "基础视图"
        ordering = ['id']


# 作业表单定义
class OperandView(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    label = models.CharField(max_length=100, blank=True, null=True, verbose_name="表单名称")
    AXIS_TYPE = [
        ('customer', '客户'),
        ('staff', '员工'),
        ('medicine', '药品'),
        ('device', '设备'),
    ]
    axis_field = models.CharField(max_length=255, choices=AXIS_TYPE, default='customer', verbose_name="关联字段")
    # subforms list: [subform1, subform2, ...]
    inquire_forms = models.ManyToManyField(SubForm, related_name="inquire_forms", verbose_name="查询子表单")
    mutate_forms = models.ManyToManyField(SubForm, related_name="mutate_forms", verbose_name="变更子表单")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "作业视图"
        verbose_name_plural = "作业视图"
        ordering = ['id']

