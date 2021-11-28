# Generated by Django 3.1.4 on 2021-09-02 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdetails',
            name='color',
            field=models.CharField(choices=[('Red', 'Red'), ('Black', 'Black'), ('White', 'White'), ('Blue', 'Blue'), ('Silver', 'Silver'), ('Green', 'Green'), ('Yellow', 'Yellow'), ('Grey', 'Grey')], default='Red', max_length=20),
        ),
        migrations.AddField(
            model_name='productdetails',
            name='ram',
            field=models.TextField(choices=[('4GB', '4GB'), ('6GB', '6GB'), ('8GB', '8GB'), ('12GB', '12GB')], default='4GB', max_length=10),
        ),
        migrations.AddField(
            model_name='productdetails',
            name='storage',
            field=models.TextField(choices=[('4GB', '4GB'), ('6GB', '6GB'), ('8GB', '8GB'), ('12GB', '12GB')], default='32GB', max_length=10),
        ),
        migrations.AlterField(
            model_name='productdetails',
            name='pr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products'),
        ),
    ]
