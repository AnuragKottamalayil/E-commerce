# Generated by Django 3.1.4 on 2021-09-01 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='logintable',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='logintable',
            name='zipcode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
