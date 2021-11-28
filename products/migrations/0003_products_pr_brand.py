# Generated by Django 3.1.4 on 2021-09-02 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210902_0307'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='pr_brand',
            field=models.CharField(choices=[('Apple', 'Apple'), ('Samsung', 'Black'), ('Redmi', 'Redmi'), ('Realme', 'Realme'), ('Oppo', 'Oppo'), ('Vivo', 'Vivo'), ('Moto', 'Moto'), ('Oneplus', 'Oneplus')], default='Apple', max_length=200, verbose_name='Brand'),
        ),
    ]