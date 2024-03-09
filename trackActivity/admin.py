from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class MyAdmin(admin.ModelAdmin):
    ordering = ('-action_time',)
     
    def has_add_permission(self, request, obj=None):
        return False
     
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
    
    def has_change_permission(self, request, obj=None):
        return False
