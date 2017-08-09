# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-08 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenta', '0006_auto_20170808_1822'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='method',
            options={'verbose_name': 'authentication method', 'verbose_name_plural': 'authentication methods'},
        ),
        migrations.AddField(
            model_name='method',
            name='method',
            field=models.CharField(default='LDAP', help_text='Authentication type', max_length=4, verbose_name='Method'),
        ),
    ]
