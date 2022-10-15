from django.db import models
from django.contrib.auth.models import User
from datetime import time

class user_settings(models.Model):
    annual_time_in_weeks = models.IntegerField(default=0)
    annual_billing_target_in_hours = models.FloatField(default=0.0)
    user_worked_time = models.FloatField(default=0.0)
    fiscal_year_start_date = models.DateField(null=True)
    working_days = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    @property
    def performance(self):
        self.worked_time = self.user_worked_time
        self.annual_target = self.annual_billing_target_in_hours

        if self.annual_target != 0:
            self.per = format(self.worked_time / self.annual_target * 100 , ".2f") + "%"
        else:
            self.per = 0
    
        return self.per

    def __str__(self):
        return self.user.username

class user_feedback(models.Model):
    feedback = models.TextField()
    date_time = models.DateTimeField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class user_entry(models.Model):
    entry_date = models.DateField()
    work_time = models.TimeField(default=time(00 , 00))
    desc = models.TextField()
    category = models.CharField(max_length=20)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class user_status(models.Model):
    status_now = models.CharField(max_length=12 , default="Inactive")
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + self.status_now

