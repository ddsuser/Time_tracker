# Generated by Django 4.0.5 on 2022-06-30 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_chart_all_functionalities', '0009_rename_status_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_settings',
            name='user_worked_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]