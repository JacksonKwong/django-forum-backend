# Generated by Django 2.2.4 on 2019-08-22 11:20

from django.db import migrations
import utils.models_field


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20190521_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlog',
            name='request_headers',
            field=utils.models_field.DictField(blank=True, null=True, verbose_name='请求头'),
        ),
    ]
