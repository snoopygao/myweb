from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Engineer(models.Model):
    state = (
        ('在职', '在职'),
        ('离职', '离职'),
    )
    name = models.CharField(max_length=10, verbose_name='姓名')
    email = models.EmailField(max_length=25, verbose_name='邮箱', null=True)
    on_job = models.CharField(max_length=5, default='在职')

    def __str__(self):
        return self.name


class Project(models.Model):
    cities = (
        ('石家庄市', '石家庄市'),
        ('唐山市', '唐山市'),
        ('秦皇岛市', '秦皇岛市'),
        ('邯郸市', '邯郸市'),
        ('邢台市', '邢台市'),
        ('保定市', '保定市'),
        ('张家口市', '张家口市'),
        ('承德市', '承德市'),
        ('沧州市', '沧州市'),
        ('廊坊市', '廊坊市'),
        ('衡水市', '衡水市'),
        ('雄安新区', '雄安新区'),
        ('不区分', '不区分'),
    )
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=100, choices=cities)
    acceptancedate = models.DateField()
    intersectiondate = models.DateField()
    opscontent = models.TextField(max_length=3000)
    patrolrequire = models.TextField(max_length=500)
    participants = models.CharField(max_length=50)
    customer = models.CharField(max_length=20)
    supervisor = models.CharField(max_length=20)
    contactors = models.TextField(max_length=200)

    class Meta:
        verbose_name = '项目列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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
    cities = (
        ('石家庄市', '石家庄市'),
        ('唐山市', '唐山市'),
        ('秦皇岛市', '秦皇岛市'),
        ('邯郸市', '邯郸市'),
        ('邢台市', '邢台市'),
        ('保定市', '保定市'),
        ('张家口市', '张家口市'),
        ('承德市', '承德市'),
        ('沧州市', '沧州市'),
        ('廊坊市', '廊坊市'),
        ('衡水市', '衡水市'),
        ('雄安新区', '雄安新区'),
        ('不区分', '不区分'),
    )
    engineer = models.ForeignKey(Engineer, on_delete=models.PROTECT, verbose_name='')
    source = models.CharField(max_length=15, choices=Q_source)
    qcategory = models.CharField(max_length=10, choices=Q_category)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    area = models.CharField(max_length=100, choices=cities)
    qdate = models.DateTimeField(auto_now_add=True, auto_now=False)
    qmethod = models.CharField(max_length=20, choices=Q_method)
    question = models.TextField(max_length=200)
    process = models.TextField(max_length=200)
    result = models.CharField(max_length=20, choices=Q_result)
    limit = models.IntegerField()
    spending = models.IntegerField()
    recorder = models.CharField(max_length=10)

    class Meta:
        verbose_name = '记录清单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question


