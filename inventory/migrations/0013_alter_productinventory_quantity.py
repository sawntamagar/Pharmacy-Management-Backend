# Generated by Django 4.1.1 on 2022-09-26 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_productinventory_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinventory',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
