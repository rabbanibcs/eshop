# Generated by Django 4.1.1 on 2022-09-23 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_category_options_alter_subcategory_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='items',
            old_name='sub_category',
            new_name='subcategory',
        ),
    ]
