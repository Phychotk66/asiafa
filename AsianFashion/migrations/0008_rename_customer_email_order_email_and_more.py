# Generated by Django 4.2.14 on 2024-08-17 02:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("AsianFashion", "0007_remove_customer_item_customer_password_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order", old_name="customer_email", new_name="email",
        ),
        migrations.RenameField(
            model_name="order", old_name="street_address", new_name="session_id",
        ),
        migrations.RenameField(
            model_name="order", old_name="apt_number", new_name="zip_code",
        ),
        migrations.AddField(
            model_name="order", name="amount", field=models.IntegerField(default=40),
        ),
        migrations.AddField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="AsianFashion.customer",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="first_name",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="is_cart_object",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="order",
            name="last_name",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="order_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="date ordered"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="street_address_line_1",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="street_address_line_2",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(default="pending review", max_length=20),
        ),
    ]
