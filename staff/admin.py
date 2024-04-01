from django.contrib import admin
from .models import Department, Staff, StaffCustomField, Degree, Designation, StaffEducation, StaffPreviousExperience

admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(StaffCustomField)
admin.site.register(Degree)
admin.site.register(Designation)
admin.site.register(StaffEducation)
admin.site.register(StaffPreviousExperience)

