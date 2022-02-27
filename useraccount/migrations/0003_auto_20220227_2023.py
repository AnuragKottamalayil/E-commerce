# Generated by Django 3.2.9 on 2022-02-27 14:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0002_auto_20220220_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='customerotp',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 20, 23, 31, 236829)),
        ),
        migrations.AlterField(
            model_name='customerotp',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 20, 23, 31, 236829)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 20, 23, 31, 236829)),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 20, 23, 31, 236829)),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 20, 23, 31, 236829)),
        ),
    ]