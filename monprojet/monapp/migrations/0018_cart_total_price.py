# Generated by Django 5.1.1 on 2024-10-17 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monapp', '0017_remove_validatedcartitem_product_supplier_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
