# Generated by Django 3.2.9 on 2022-02-06 10:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_products_pr_quantity'),
        ('useraccount', '0024_auto_20220206_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product_variation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productvariation'),
        ),
        migrations.AlterField(
            model_name='customerotp',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 15, 38, 47, 843134)),
        ),
        migrations.AlterField(
            model_name='customerotp',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 15, 38, 47, 843134)),
        ),
    ]