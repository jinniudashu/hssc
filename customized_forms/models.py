from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from core.models import Form
from time import time
from pypinyin import lazy_pinyin

# 字段定义
# 字符字段
class CharacterField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="组件名称")
    CHAR_TYPE = [('CharField', '单行文本'), ('TextField', '多行文本')]
    type = models.CharField(max_length=50, choices=CHAR_TYPE, default='CharField', verbose_name="类型")
    length = models.PositiveSmallIntegerField(default=255, verbose_name="字符长度")
    # component = GenericRelation(to='Component')

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}_{int(time())}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "字符字段"
        verbose_name_plural = "字符字段"


# 数值字段
class NumberField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="组件名称")
    NUMBER_TYPE = [('IntegerField', '整数'), ('DecimalField', '固定精度小数'), ('FloatField', '浮点数')]
    type = models.CharField(max_length=50, choices=NUMBER_TYPE, default='IntegerField', verbose_name="类型")
    max_digits = models.PositiveSmallIntegerField(default=10, verbose_name="最大位数", null=True, blank=True)
    decimal_places = models.PositiveSmallIntegerField(default=2, verbose_name="小数位数", null=True, blank=True)
    standard_value = models.FloatField(null=True, blank=True, verbose_name="标准值")
    up_limit = models.FloatField(null=True, blank=True, verbose_name="上限")
    down_limit = models.FloatField(null=True, blank=True, verbose_name="下限")
    display_unit = models.BooleanField(default=False, verbose_name="显示单位")
    unit = models.CharField(max_length=50, null=True, blank=True, verbose_name="单位")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}_{int(time())}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "数值字段"
        verbose_name_plural = "数值字段"


# 日期时间字段
class DTField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="组件名称")
    DT_TYPE = [('DateField', '日期'), ('DateTimeField', '日期时间')]
    type = models.CharField(max_length=50, choices=DT_TYPE, default='DateField', verbose_name="类型")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}_{int(time())}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "日期字段"
        verbose_name_plural = "日期字段"


# 选择字段
class ChoiceField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="组件名称")
    CHOICE_TYPE = [('Select', '下拉单选'), ('RadioSelect', '单选按钮列表'), ('CheckboxSelectMultiple', '复选框列表'), ('SelectMultiple', '下拉多选')]
    type = models.CharField(max_length=50, choices=CHOICE_TYPE, default='ChoiceField', verbose_name="类型")
    options = models.TextField(max_length=1024, null=True, blank=True, verbose_name="选项", help_text="每行一个选项, 最多100个")
    is_dic = models.BooleanField(default=False, verbose_name="是否字典")
    first_default = models.BooleanField(default=False, verbose_name="默认选中第一个")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}_{int(time())}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "选择字段"
        verbose_name_plural = "选择字段"


# 关联字段
class RelatedField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="组件名称")
    related_content = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    related_field = models.CharField(max_length=100, null=True, blank=True, verbose_name="关联字段")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}_{int(time())}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "关联字段"
        verbose_name_plural = "关联字段"


# 计算字段
class ComputeField(models.Model):
    pass


# 组件清单
class Component(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="组件名称", null=True, blank=True)

    q = Q(app_label='customized_forms') & (
        Q(model = 'characterfield') | 
        Q(model = 'numberfield') | 
        Q(model = 'dtfield') | 
        Q(model = 'choicefield') | 
        Q(model = 'relatedfield') | 
        Q(model = 'computefield')
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=q, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "组件清单"
        verbose_name_plural = "组件清单"
        ordering = ['id']


# 基础表单定义
class BaseModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="表单名称", null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    components = models.ManyToManyField(Component, verbose_name="组件清单")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}_{int(time())}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "基础表单"
        verbose_name_plural = "基础表单"
        ordering = ['id']


# 基础视图定义
class BaseForm(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    label = models.CharField(max_length=100, null=True, blank=True, verbose_name="视图名称")
    basemodel = models.ForeignKey(BaseModel, on_delete=models.CASCADE, verbose_name="基础表单")
    is_inquiry = models.BooleanField(default=False, verbose_name="仅用于查询")
    FORM_STYLE = [('detail', '详情'),('list', '列表')]
    style = models.CharField(max_length=50, choices=FORM_STYLE, default='detail', verbose_name='风格')
    display_fields = models.TextField(max_length=1024, blank=True, null=True, verbose_name="表单字段")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "基础视图"
        verbose_name_plural = "基础视图"
        ordering = ['id']


# 作业视图定义
class OperandView(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    label = models.CharField(max_length=100, blank=True, null=True, verbose_name="表单名称")
    AXIS_TYPE = [
        ('customer', '客户'),
        ('staff', '员工'),
        ('medicine', '药品'),
        ('device', '设备'),
    ]
    axis_field = models.CharField(max_length=255, choices=AXIS_TYPE, default='customer', verbose_name="业务主键")
    inquire_forms = models.ManyToManyField(BaseForm, limit_choices_to={'is_inquiry': True}, related_name="inquire_forms", verbose_name="查询视图")
    mutate_forms = models.ManyToManyField(BaseForm, limit_choices_to={'is_inquiry': False}, related_name="mutate_forms", verbose_name="变更视图")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}_{int(time())}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "作业视图"
        verbose_name_plural = "作业视图"
        ordering = ['id']

# 把model转为JSON
# json.loads(serializers.serialize('json',[ct1.content_object])[1:-1])['fields']
