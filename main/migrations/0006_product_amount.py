# Generated by Django 4.1.3 on 2022-11-08 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_sale_created_at_alter_sale_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='在庫数'),
        ),
    ]
