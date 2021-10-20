# Generated by Django 3.2.7 on 2021-10-20 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0004_purchase_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
