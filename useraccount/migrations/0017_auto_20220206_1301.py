# Generated by Django 3.2.9 on 2022-02-06 07:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0016_auto_20220130_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerotp',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 13, 1, 16, 781935)),
        ),
        migrations.AlterField(
            model_name='customerotp',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 13, 1, 16, 781935)),
        ),
    ]