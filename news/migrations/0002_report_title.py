# Generated by Django 5.2.1 on 2025-07-14 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='title',
            field=models.CharField(default='dlewfbhoerfbwojgnrtnoe', max_length=1024),
            preserve_default=False,
        ),
    ]
