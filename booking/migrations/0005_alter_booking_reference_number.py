# Generated by Django 4.0.4 on 2022-06-23 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_booking_reference_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='reference_number',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
