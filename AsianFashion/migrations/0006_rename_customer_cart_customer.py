# Generated by Django 4.2.14 on 2024-08-14 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("AsianFashion", "0005_alter_item_height_cm_alter_item_length_cm_and_more"),
    ]

    operations = [
        migrations.RenameModel(old_name="Customer_Cart", new_name="Customer",),
    ]
