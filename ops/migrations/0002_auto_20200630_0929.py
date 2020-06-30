# Generated by Django 3.0.7 on 2020-06-30 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
        ('ops', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opsrecord',
            options={'verbose_name': '运维记录清单', 'verbose_name_plural': '运维记录清单'},
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.City', verbose_name='所属地市'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='engineer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ops.Engineer', verbose_name='处理人'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='limit',
            field=models.DecimalField(decimal_places=1, max_digits=3, verbose_name='处理时限(h)'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='process',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='处理过程'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Project', verbose_name='所属项目'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='qcategory',
            field=models.CharField(choices=[('技术支持', '技术支持'), ('故障处理', '故障处理'), ('性能调优', '性能调优'), ('问题咨询', '问题咨询'), ('商务售前支撑', '商务售前支撑')], default='故障处理', max_length=10, verbose_name='事件类型'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='qdate',
            field=models.DateTimeField(auto_now=True, verbose_name='致电时间'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='qmethod',
            field=models.CharField(choices=[('电话', '电话'), ('微信/QQ', '微信/QQ'), ('邮件', '邮件')], default='电话', max_length=20, verbose_name='致电方式'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='question',
            field=models.TextField(max_length=500, verbose_name='问题描述'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='recorder',
            field=models.CharField(max_length=10, verbose_name='记录人'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='result',
            field=models.CharField(choices=[('正在处理', '正在处理'), ('处理完成', '处理完成'), ('挂起', '挂起')], default='处理完成', max_length=20, verbose_name='处理结果'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='source',
            field=models.CharField(choices=[('客户致电', '客户致电'), ('主动发现', '主动发现'), ('合作单位致电', '合作单位致电'), ('内部支持', '内部支持')], default='客户致电', max_length=15, verbose_name='事件来源'),
        ),
        migrations.AlterField(
            model_name='opsrecord',
            name='spending',
            field=models.DecimalField(decimal_places=1, max_digits=3, verbose_name='实际处理时长(h)'),
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]