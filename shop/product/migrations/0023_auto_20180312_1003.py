# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-12 10:03
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_auto_20180310_1212'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('active_product', django.db.models.manager.Manager()),
            ],
        ),
    ]
