# Generated by Django 4.2.7 on 2024-04-23 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_alter_trademeet_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='type',
            field=models.CharField(choices=[('Spam', 'Spam'), ('Inappropriate Content', 'Inappropriate Content'), ('Didnot Appear', 'Didnot Appear'), ('Fake Book', 'Fake Book'), ('Wrong Trade Meet Place', 'Wrong Trade Meet Place'), ('Other', 'Other')], max_length=50),
        ),
    ]
