# Generated by Django 3.2.9 on 2022-02-06 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20220206_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='pr_quantity',
            field=models.IntegerField(blank=True, null=True, verbose_name='Product Quantity'),
        ),
    ]
