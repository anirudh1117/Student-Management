from django.contrib import admin
from .models import Exam, CourseSchedule, Marks
# Register your models here.
admin.site.register(Exam)
admin.site.register(CourseSchedule)
admin.site.register(Marks)
