# Generated by Django 5.2.1 on 2025-05-25 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bout',
            name='day',
            field=models.IntegerField(default=25),
            preserve_default=False,
        ),
    ]
