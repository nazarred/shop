# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-17 11:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20180217_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='add_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
