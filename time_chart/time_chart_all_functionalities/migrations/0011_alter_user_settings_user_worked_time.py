# Generated by Django 4.0.5 on 2022-06-30 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_chart_all_functionalities', '0010_user_settings_user_worked_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_settings',
            name='user_worked_time',
            field=models.IntegerField(default=0),
        ),
    ]
