# Generated by Django 4.0.5 on 2022-10-13 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_chart_all_functionalities', '0016_alter_user_settings_annual_billing_target_in_hours_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_settings',
            name='annual_billing_target_in_hours',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='user_settings',
            name='user_worked_time',
            field=models.FloatField(default=0.0),
        ),
    ]
