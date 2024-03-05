from django.db import models

class ExamSchedule(models.Model):
    sl = models.CharField(max_length=3)
    course = models.CharField(max_length=8)
    section = models.CharField(max_length=4)
    mid_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=10)
    # mode = models.CharField(max_length=50, null=True)
