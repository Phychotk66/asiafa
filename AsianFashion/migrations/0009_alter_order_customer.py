# Generated by Django 4.2.14 on 2024-08-17 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("AsianFashion", "0008_rename_customer_email_order_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="AsianFashion.customer",
            ),
        ),
    ]