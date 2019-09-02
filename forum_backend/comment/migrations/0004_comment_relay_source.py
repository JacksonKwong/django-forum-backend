# Generated by Django 2.1.7 on 2019-06-17 08:11

from django.db import migrations
import utils.models_field


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_remove_comment_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='relay_source',
            field=utils.models_field.DictField(blank=True, null=True, verbose_name='转发源'),
        ),
    ]