# Generated by Django 5.1.1 on 2024-10-17 22:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monapp', '0018_cart_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validatedcartitem',
            name='cart_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monapp.cartitem'),
        ),
        migrations.AlterField(
            model_name='validatedcartitem',
            name='validated_cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='monapp.validatedcart'),
        ),
    ]
