# Generated by Django 4.1.1 on 2022-10-01 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_items_discount_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='discount_price',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
