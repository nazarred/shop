# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-27 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_remove_productincart_in_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='productincart',
            name='in_order',
            field=models.BooleanField(default=False),
        ),
    ]
