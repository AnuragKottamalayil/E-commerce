# Generated by Django 3.2.9 on 2022-01-30 11:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0014_auto_20220130_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerotp',
            name='verified',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='customerotp',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 30, 17, 16, 52, 474990)),
        ),
        migrations.AlterField(
            model_name='customerotp',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 30, 17, 16, 52, 474990)),
        ),
    ]
