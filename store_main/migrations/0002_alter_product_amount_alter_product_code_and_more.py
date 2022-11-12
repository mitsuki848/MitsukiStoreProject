# Generated by Django 4.1.3 on 2022-11-11 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='在庫数'),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='商品コード'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='価格'),
        ),
    ]
