# Generated by Django 4.0.5 on 2022-06-28 08:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('time_chart_all_functionalities', '0008_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='status',
            new_name='user_status',
        ),
    ]