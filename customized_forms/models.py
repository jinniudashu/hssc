from django.db import models

# 组件
class Component(models.Model):
    # Base field type
    CHAR_FIELD = {}
    TEXT_FIELD = {}
    INTEGER_FIELD = {}
    FLOAT_FIELD = {}
    SELECT_FIELD = {}
    DATETIME_FIELD = {}
    CALCULATED_FIELD = {}

    FIELD_TYPE = [
        ('char_field', CHAR_FIELD),
        ('text_field', TEXT_FIELD),
        ('integer_field', INTEGER_FIELD),
        ('float_field', FLOAT_FIELD),
        ('select_field', SELECT_FIELD),
        ('datetime_field', DATETIME_FIELD),
        ('calculated_field', CALCULATED_FIELD)
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="名称")
    label = models.CharField(max_length=100, verbose_name="组件名称")
    field_type = models.CharField(max_length=100, choices=FIELD_TYPE, verbose_name="类型")
    attribute = models.JSONField(verbose_name="属性")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "组件"
        verbose_name_plural = "组件"
        ordering = ['id']

# 子表单
class SubForm(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    label = models.CharField(max_length=100, verbose_name="子表单")
    # components: [component1, component2, ...]
    components = models.CharField(max_length=255, verbose_name="组件清单")
    FORM_STYLE = [
		('detail', '详情'),
		('list', '列表'),
	]
    style = models.CharField(max_length=100, choices=FORM_STYLE, default='detail', verbose_name='风格')

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "子表单"
        verbose_name_plural = "子表单"
        ordering = ['id']


# 作业表单
class Operand_Form(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    label = models.CharField(max_length=100, blank=True, null=True, verbose_name="表单名称")
    meta_form = models.ForeignKey(SubForm, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="元表单")
    # subforms list: [subform1, subform2, ...]
    subforms = models.CharField(max_length=255, verbose_name="子表单集")
    LAYOUT_STYLE = [
		('monomer', '单体'),
		('pagination', '分页'),
	]
    layout = models.CharField(max_length=100, choices=LAYOUT_STYLE, default='monomer', verbose_name='布局')

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        
        # create model

        # create view

        # create form
        
        # create template

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "作业表单"
        verbose_name_plural = "作业表单"
        ordering = ['id']
