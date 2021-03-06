# Generated by Django 3.2.7 on 2021-10-06 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.product'),
        ),
        migrations.AlterModelTable(
            name='cart',
            table='cart',
        ),
        migrations.AlterModelTable(
            name='entry',
            table='entry',
        ),
    ]
