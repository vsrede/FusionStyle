# Generated by Django 4.2.4 on 2023-08-23 16:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0007_alter_customer_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="email",
            field=models.EmailField(
                error_messages={"unique": "A user with that email already exists."},
                max_length=254,
                unique=True,
                verbose_name="email address",
            ),
        ),
    ]
