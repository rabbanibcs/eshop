# Generated by Django 4.1.1 on 2022-09-22 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='items',
            options={'verbose_name_plural': 'Items'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name_plural': 'SubCategory'},
        ),
        migrations.AlterModelTable(
            name='items',
            table='Items',
        ),
        migrations.AlterModelTable(
            name='subcategory',
            table='SubCategory',
        ),
    ]
