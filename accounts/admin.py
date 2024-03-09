from typing import Any
from django.contrib import admin
from django import forms
from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, Address
from school.models import School
from utils.commonFunction import get_school_list

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = UserAccount

class UserAccountAdminForm(forms.ModelForm):
    select_school = forms.ChoiceField(required=True, choices=get_school_list())

    def __init__(self, *args, **kwargs):
        super(UserAccountAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['select_school'].initial = instance.school.id

@admin.register(UserAccount)
class MyAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'first_name', 'last_name', 'is_staff']
    list_filter = ['role','gender']
    exclude = ('school',)
    ordering = ['role']
    form = UserAccountAdminForm

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        school_id = request.POST['select_school']
        schoolObj = School.objects.filter(id=school_id)
        if schoolObj.first():
            schoolObj = schoolObj[0]
        else:
            schoolObj = None
        obj.school = schoolObj
        obj.password = make_password(obj.password,hasher='default')
        return super().save_model(request, obj, form, change)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        user_obj_list = super().get_queryset(request)
        if request.user.is_superuser:
            return user_obj_list
        else:
            if request.user.school:
                user_obj_list = user_obj_list.filter(school = request.user.school)
                return user_obj_list
            else:
                return []

admin.site.register(Address)
