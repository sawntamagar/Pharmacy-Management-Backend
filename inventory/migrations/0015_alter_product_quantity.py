# Generated by Django 4.1.1 on 2022-09-26 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_remove_productinventory_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
