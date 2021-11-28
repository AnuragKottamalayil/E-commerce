# Generated by Django 3.1.4 on 2021-09-02 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_products_pr_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetails',
            name='storage',
            field=models.TextField(choices=[('32GB', '32GB'), ('64GB', '64GB'), ('128GB', '128GB'), ('512GB', '512GB')], default='32GB', max_length=10),
        ),
    ]
