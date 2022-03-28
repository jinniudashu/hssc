
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from pypinyin import Style, lazy_pinyin

class IcpcBase(models.Model):
    icpc_code = models.CharField(max_length=5, unique=True, blank=True, null=True, verbose_name="icpc码")
    icode = models.CharField(max_length=3, blank=True, null=True, verbose_name="分类码")
    iname = models.CharField(max_length=255, blank=True, null=True, verbose_name="名称")
    iename = models.CharField(max_length=255, blank=True, null=True, verbose_name="English Name")
    include = models.CharField(max_length=1024, blank=True, null=True, verbose_name="包含")
    criteria = models.CharField(max_length=1024, blank=True, null=True, verbose_name="准则")
    exclude = models.CharField(max_length=1024, blank=True, null=True, verbose_name="排除")
    consider = models.CharField(max_length=1024, blank=True, null=True, verbose_name="考虑")
    icd10 = models.CharField(max_length=8, blank=True, null=True, verbose_name="ICD10")
    icpc2 = models.CharField(max_length=10, blank=True, null=True, verbose_name="ICPC2")
    note = models.CharField(max_length=1024, blank=True, null=True, verbose_name="备注")
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")

    def __str__(self):
        return str(self.iname)

    class Meta:
        abstract = True


# ICPC子类抽象类
class IcpcSubBase(IcpcBase):
    def save(self, *args, **kwargs):
        if self.iname:
            self.pym = ''.join(lazy_pinyin(self.iname, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# ICPC总表
class Icpc(IcpcBase):
    subclass = models.CharField(max_length=255, blank=True, null=True, verbose_name="ICPC子类")

    class Meta:
        verbose_name = "ICPC总表"
        verbose_name_plural = verbose_name


class Icpc1_register_logins(IcpcSubBase):
    class Meta:
        verbose_name = '注册登录（行政管理）'
        verbose_name_plural = verbose_name


class Icpc2_reservation_investigations(IcpcSubBase):
    class Meta:
        verbose_name = '预约咨询调查（行政管理）'
        verbose_name_plural = verbose_name


class Icpc3_symptoms_and_problems(IcpcSubBase):
    class Meta:
        verbose_name = '症状和问题'
        verbose_name_plural = verbose_name


class Icpc4_physical_examination_and_tests(IcpcSubBase):
    class Meta:
        verbose_name = '体格和其他检查'
        verbose_name_plural = verbose_name


class Icpc5_evaluation_and_diagnoses(IcpcSubBase):
    class Meta:
        verbose_name = '评估和诊断'
        verbose_name_plural = verbose_name


class Icpc6_prescribe_medicines(IcpcSubBase):
    class Meta:
        verbose_name = '开药'
        verbose_name_plural = verbose_name


class Icpc7_treatments(IcpcSubBase):
    class Meta:
        verbose_name = '治疗'
        verbose_name_plural = verbose_name


class Icpc8_other_health_interventions(IcpcSubBase):
    class Meta:
        verbose_name = '其他健康干预'
        verbose_name_plural = verbose_name


class Icpc9_referral_consultations(IcpcSubBase):
    class Meta:
        verbose_name = '转诊会诊'
        verbose_name_plural = verbose_name


class Icpc10_test_results_and_statistics(IcpcSubBase):
    class Meta:
        verbose_name = '检查结果和统计'
        verbose_name_plural = verbose_name

@receiver(post_save, sender=Icpc1_register_logins, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc2_reservation_investigations, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc3_symptoms_and_problems, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc4_physical_examination_and_tests, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc5_evaluation_and_diagnoses, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc6_prescribe_medicines, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc7_treatments, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc8_other_health_interventions, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc9_referral_consultations, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc10_test_results_and_statistics, weak=True, dispatch_uid=None)
def icpc_post_save_handler(sender, instance, created, **kwargs):
	if created:
		Icpc.objects.create(
			icpc_code=instance.icpc_code,
			icode=instance.icode,
			iname=instance.iname,
			iename=instance.iename,
			include=instance.include,
			criteria=instance.criteria,
			exclude=instance.exclude,
			consider=instance.consider,
			icd10=instance.icd10,
			icpc2=instance.icpc2,
			note=instance.note,
			pym=instance.pym,
			subclass=instance._meta.object_name
		)
	else:
		Icpc.objects.filter(icpc_code=instance.icpc_code).update(
			icode=instance.icode,
			iname=instance.iname,
			iename=instance.iename,
			include=instance.include,
			criteria=instance.criteria,
			exclude=instance.exclude,
			consider=instance.consider,
			icd10=instance.icd10,
			icpc2=instance.icpc2,
			note=instance.note,
			pym=instance.pym,
			subclass=instance._meta.object_name
		)

@receiver(post_delete, sender=Icpc1_register_logins, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc2_reservation_investigations, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc3_symptoms_and_problems, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc4_physical_examination_and_tests, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc5_evaluation_and_diagnoses, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc6_prescribe_medicines, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc7_treatments, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc8_other_health_interventions, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc9_referral_consultations, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc10_test_results_and_statistics, weak=True, dispatch_uid=None)
def icpc_post_delete_handler(sender, instance, **kwargs):
	Icpc.objects.filter(icpc_code=instance.icpc_code).delete()
