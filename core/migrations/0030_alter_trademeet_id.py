# Generated by Django 4.2.7 on 2024-04-07 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_trademeet_receiver_trademeet_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trademeet',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
