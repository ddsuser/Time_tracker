# Generated by Django 4.0.5 on 2022-07-12 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_chart_all_functionalities', '0015_alter_user_settings_annual_time_in_weeks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_settings',
            name='annual_billing_target_in_hours',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='user_settings',
            name='annual_time_in_weeks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user_settings',
            name='user_worked_time',
            field=models.FloatField(default=1.0),
        ),
    ]
