# Generated by Django 2.1.7 on 2019-05-21 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_userlog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userlog',
            options={'ordering': ['-created'], 'verbose_name': '用户日志', 'verbose_name_plural': '用户日志'},
        ),
        migrations.AddField(
            model_name='userlog',
            name='request_ip',
            field=models.GenericIPAddressField(blank=True, null=True, unpack_ipv4=True, verbose_name='请求IP'),
        ),
    ]
