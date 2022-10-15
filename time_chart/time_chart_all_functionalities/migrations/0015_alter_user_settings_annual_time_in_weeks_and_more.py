# Generated by Django 4.0.5 on 2022-07-12 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_chart_all_functionalities', '0014_alter_user_settings_fiscal_year_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_settings',
            name='annual_time_in_weeks',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user_settings',
            name='fiscal_year_start_date',
            field=models.DateField(null=True),
        ),
    ]