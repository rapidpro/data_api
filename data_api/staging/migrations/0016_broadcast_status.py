# Generated by Django 2.2.3 on 2019-07-24 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staging', '0015_auto_20190724_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='broadcast',
            name='status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
