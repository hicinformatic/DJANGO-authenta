# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-08 21:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('authenta', '0008_auto_20170808_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='method',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creation date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='method',
            name='date_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Last modification date'),
        ),
        migrations.AddField(
            model_name='method',
            name='groups',
            field=models.ManyToManyField(blank=True, to='authenta.Group', verbose_name='Groups associated'),
        ),
        migrations.AddField(
            model_name='method',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active status'),
        ),
        migrations.AddField(
            model_name='method',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Staff status'),
        ),
        migrations.AddField(
            model_name='method',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='Superuser status'),
        ),
        migrations.AddField(
            model_name='method',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='Permissions associated'),
        ),
        migrations.AddField(
            model_name='method',
            name='update_by',
            field=models.CharField(default='test', editable=False, max_length=254, verbose_name='Update by'),
            preserve_default=False,
        ),
    ]
