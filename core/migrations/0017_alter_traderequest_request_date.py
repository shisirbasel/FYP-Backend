# Generated by Django 4.2.7 on 2024-03-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_traderequest_request_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traderequest',
            name='request_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
