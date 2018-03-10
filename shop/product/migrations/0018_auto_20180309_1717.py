# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-09 17:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0017_auto_20180308_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='productincart',
            name='session_key',
            field=models.CharField(blank=True, max_length=42, null=True),
        ),
        migrations.AddField(
            model_name='productincart',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_in_cart', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]