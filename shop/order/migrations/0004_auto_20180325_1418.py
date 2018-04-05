# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-25 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20180325_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinorder',
            name='product',
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='product.ProductInCart'),
        ),
        migrations.DeleteModel(
            name='ProductInOrder',
        ),
    ]
