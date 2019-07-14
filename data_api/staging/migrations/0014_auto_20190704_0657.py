# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-07-04 06:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staging', '0013_remove_duplicate_uuids_20190704_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='uuid',
            field=models.UUIDField(db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='campaignevent',
            name='uuid',
            field=models.UUIDField(db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='uuid',
            field=models.UUIDField(db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='uuid',
            field=models.UUIDField(db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='flow',
            name='uuid',
            field=models.UUIDField(db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='flowstart',
            name='uuid',
            field=models.UUIDField(db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='uuid',
            field=models.UUIDField(db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='label',
            name='uuid',
            field=models.UUIDField(db_index=True, unique=True),
        ),
    ]
