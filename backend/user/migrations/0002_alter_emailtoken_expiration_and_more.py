# Generated by Django 4.1.1 on 2022-11-02 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtoken',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 2, 12, 34, 3, 109123, tzinfo=datetime.timezone.utc), verbose_name='expiration'),
        ),
        migrations.AlterField(
            model_name='fmctoken',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 2, 12, 40, 3, 125445, tzinfo=datetime.timezone.utc), verbose_name='expiration'),
        ),
        migrations.AlterField(
            model_name='passwordchangerequestmodel',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 2, 12, 40, 3, 125445, tzinfo=datetime.timezone.utc), verbose_name='expiration'),
        ),
    ]
