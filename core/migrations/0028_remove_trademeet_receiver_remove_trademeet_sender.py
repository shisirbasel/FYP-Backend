# Generated by Django 4.2.7 on 2024-04-07 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_trademeet_receiver_trademeet_sender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trademeet',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='trademeet',
            name='sender',
        ),
    ]
