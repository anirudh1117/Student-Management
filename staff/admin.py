from django.contrib import admin
from .models import Department, Staff, StaffCustomField

admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(StaffCustomField)

# Register your models here.
