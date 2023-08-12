# Generated by Django 4.2.4 on 2023-08-12 13:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customer",
            options={
                "ordering": ("last_name",),
                "verbose_name": "Customer",
                "verbose_name_plural": "Customers",
            },
        ),
        migrations.AlterField(
            model_name="customer",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to="customer/avatar_customer/"
            ),
        ),
    ]
