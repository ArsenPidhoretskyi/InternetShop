# Generated by Django 3.2.7 on 2021-10-06 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20211007_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
