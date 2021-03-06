# Generated by Django 3.2.7 on 2021-10-10 16:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0003_alter_discount_value'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discount',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='discount',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='discount',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
