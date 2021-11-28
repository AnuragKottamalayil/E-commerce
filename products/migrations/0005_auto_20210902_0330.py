# Generated by Django 3.1.4 on 2021-09-02 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20210902_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdetails',
            name='battery',
            field=models.TextField(default='3000 mAh'),
        ),
        migrations.AddField(
            model_name='productdetails',
            name='display',
            field=models.CharField(choices=[('Amoled', 'Amoled'), ('SAmoled', 'SAmoled'), ('Oled', 'Oled'), ('LCD', 'LCD'), ('SuperRetina', 'SuperRetina'), ('SuperRetina XDR', 'SuperRetina XDR')], default='LCD', max_length=30),
        ),
        migrations.AddField(
            model_name='productdetails',
            name='removable_battery',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=30),
        ),
    ]