# Generated by Django 4.2.14 on 2024-08-17 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("AsianFashion", "0010_choice_item"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer_cart",
            name="choice",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="AsianFashion.choice",
            ),
        ),
    ]