# Generated by Django 4.2.7 on 2024-04-14 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_rename_traderequest_rating_traderequest_trademeet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trademeet',
            name='is_accepted',
        ),
        migrations.AddField(
            model_name='trademeet',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=50),
        ),
    ]
