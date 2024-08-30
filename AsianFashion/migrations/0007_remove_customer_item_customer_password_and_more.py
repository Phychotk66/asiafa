# Generated by Django 4.2.14 on 2024-08-14 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("AsianFashion", "0006_rename_customer_cart_customer"),
    ]

    operations = [
        migrations.RemoveField(model_name="customer", name="item",),
        migrations.AddField(
            model_name="customer",
            name="password",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="customer", name="email", field=models.CharField(max_length=20),
        ),
        migrations.CreateModel(
            name="Customer_Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="AsianFashion.customer"
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="AsianFashion.item"
                    ),
                ),
            ],
        ),
    ]
