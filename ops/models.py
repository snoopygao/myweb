from django.db import models
from django.contrib.auth.models import User
from cmdb.models import City, Project
import django.utils.timezone as timezone
from django.template.defaultfilters import truncatechars


class OpsRecord(models.Model):
    Q_source = (
        ('客户致电', '客户致电'),
        ('主动发现', '主动发现'),
        ('合作单位致电', '合作单位致电'),
        ('内部支持', '内部支持'),
    )
    Q_category = (
        ('技术支持', '技术支持'),
        ('故障处理', '故障处理'),
        ('性能调优', '性能调优'),
        ('问题咨询', '问题咨询'),
        ('商务售前支撑', '商务售前支撑'),
    )
    Q_method = (
        ('电话', '电话'),
        ('微信/QQ', '微信/QQ'),
        ('邮件', '邮件'),
    )
    Q_result = (
        ('正在处理', '正在处理'),
        ('处理完成', '处理完成'),
        ('挂起', '挂起'),
    )
    engineer = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, verbose_name='工程师')
    source = models.CharField(max_length=15, choices=Q_source, default='客户致电', verbose_name='事件来源')
    qcategory = models.CharField(max_length=10, choices=Q_category, default='故障处理', verbose_name='事件类型')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    area = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='所属地市')
    qdate = models.DateTimeField(verbose_name='致电(发现)时间', default=timezone.now)
    qmethod = models.CharField(max_length=20, choices=Q_method, null=True, blank=True, verbose_name='致电方式')
    question = models.TextField(max_length=500, verbose_name='问题描述')

    @property
    def short_q(self):
        return truncatechars(self.question, 20)
    short_q.fget.short_description = '事件描述'

    process = models.TextField(max_length=500, null=True, blank=True, verbose_name='处理过程', help_text='处理时间：操作内容')

    @property
    def short_p(self):
        return truncatechars(self.process, 20)
    short_p.fget.short_description = '处理过程'
    result = models.CharField(max_length=20, choices=Q_result, default='正在处理', verbose_name='处理结果')
    limit = models.DecimalField(max_digits=3, decimal_places=1, default=4.0, verbose_name='处理时限(h)')
    spending = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='实际处理时长(h)')

    class Meta:
        verbose_name = '运维记录清单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question


