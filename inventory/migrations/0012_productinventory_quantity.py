# Generated by Django 4.1.1 on 2022-09-26 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinventory',
            name='quantity',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
