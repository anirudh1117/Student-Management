from django.contrib import admin
from .models import Leave, LeaveType

admin.site.register(Leave)
admin.site.register(LeaveType)