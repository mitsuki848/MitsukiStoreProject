# Generated by Django 4.1.3 on 2022-11-08 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_sale_product_alter_sale_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='販売日'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='商品単価'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total_price',
            field=models.PositiveIntegerField(default=0, verbose_name='小計'),
        ),
    ]
