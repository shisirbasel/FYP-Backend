# Generated by Django 4.2.7 on 2024-03-28 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_traderequest_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='traderequest',
            unique_together={('user', 'requested_book', 'status')},
        ),
    ]
