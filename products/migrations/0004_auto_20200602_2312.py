# Generated by Django 3.0.3 on 2020-06-02 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['title', 'price']},
        ),
    ]
