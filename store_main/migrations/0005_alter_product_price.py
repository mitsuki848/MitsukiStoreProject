# Generated by Django 4.1.3 on 2022-11-11 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_main', '0004_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(verbose_name='価格'),
        ),
    ]
