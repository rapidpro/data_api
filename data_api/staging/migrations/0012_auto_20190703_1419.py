# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-07-03 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staging', '0011_auto_20180920_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='created_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]