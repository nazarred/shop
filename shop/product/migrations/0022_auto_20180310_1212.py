# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-10 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_auto_20180309_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrating',
            name='rating',
            field=models.CharField(default='0', max_length=6),
        ),
    ]