# Generated by Django 3.0.3 on 2020-06-03 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200602_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='products',
            name='quantity',
            field=models.DecimalField(decimal_places=0, max_digits=3),
        ),
    ]
