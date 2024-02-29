# Generated by Django 5.0.2 on 2024-02-29 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0005_alter_viewedproduct_viewed_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="discount_price",
        ),
        migrations.AddField(
            model_name="product",
            name="discount",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="viewedproduct",
            name="viewed",
            field=models.BooleanField(default=2),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="Discount",
        ),
    ]
