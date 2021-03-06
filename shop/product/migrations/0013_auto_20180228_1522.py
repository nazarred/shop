# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-28 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20180224_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='prod', to='product.ProductImage'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.Product'),
        ),
    ]
