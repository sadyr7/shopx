# Generated by Django 5.0.2 on 2024-02-29 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0003_product_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="products/%Y/%m/%d"
            ),
        ),
    ]