# Generated by Django 4.2.7 on 2024-05-02 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_delete_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
