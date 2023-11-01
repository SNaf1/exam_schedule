from django.contrib import admin
from .models import ExamSchedule

class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ('sl', 'course', 'section', 'mid_date', 'start_time', 'end_time', 'room')
    list_filter = ('course', 'mid_date')

admin.site.register(ExamSchedule, ExamScheduleAdmin)
