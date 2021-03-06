# Generated by Django 2.1.7 on 2019-05-21 03:44

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import utils.models_field


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190430_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('username', models.CharField(blank=True, max_length=150, null=True, verbose_name='所属用户名')),
                ('request_path', models.CharField(blank=True, max_length=150, null=True, verbose_name='请求路径')),
                ('request_type', models.CharField(blank=True, choices=[('GET', 'GET'), ('POST', 'POST'), ('DELETE', 'DELETE'), ('PUT', 'PUT'), ('PATH', 'PATH')], max_length=10, null=True, verbose_name='请求类型')),
                ('request_data', utils.models_field.DictField(unique=False,blank=True, null=True, verbose_name='请求数据')),
                ('request_meta', utils.models_field.DictField(unique=False,blank=True, null=True, verbose_name='请求元数据')),
                ('response_status_code', models.CharField(unique=False,blank=True, max_length=10, null=True, verbose_name='响应状态码')),
                ('response_data', utils.models_field.DictField(unique=False,blank=True, null=True, verbose_name='响应数据')),
            ],
            options={
                'verbose_name': '用户配置',
                'verbose_name_plural': '用户配置',
                'ordering': ['-created'],
            },
        ),
    ]
