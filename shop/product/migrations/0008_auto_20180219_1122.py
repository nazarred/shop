# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-19 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_productrating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='nmb_of_rating',
        ),
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sum_rating',
        ),
        migrations.AlterField(
            model_name='productrating',
            name='rating',
            field=models.CharField(choices=[('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], default='0', max_length=6),
        ),
    ]
