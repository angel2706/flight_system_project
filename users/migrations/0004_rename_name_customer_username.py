# Generated by Django 3.2.5 on 2022-06-22 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_username_customer_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='name',
            new_name='username',
        ),
    ]
