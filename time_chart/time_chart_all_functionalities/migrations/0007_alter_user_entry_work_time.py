# Generated by Django 4.0.5 on 2022-06-24 10:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_chart_all_functionalities', '0006_remove_user_entry_worked_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_entry',
            name='work_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]