# Generated by Django 3.2.9 on 2022-02-27 14:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0004_auto_20220227_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customerotp',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 20, 25, 4, 95805)),
        ),
        migrations.AlterField(
            model_name='customerotp',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 20, 25, 4, 95805)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 20, 25, 4, 95805)),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 20, 25, 4, 95805)),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 20, 25, 4, 95805)),
        ),
    ]