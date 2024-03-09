from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django import forms
from typing import Any

from utils.commonFunction import get_school_list, get_initials_from_string
from school.models import School

admin.site.unregister(Group)


class GroupAdminForm(forms.ModelForm):
    select_school = forms.ChoiceField(required=True, choices=get_school_list())

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.request:
            if not self.request.user.is_superuser:
                self.fields['select_school'].initial = self.request.user.school.id


@admin.register(Group)
class GroupCustomAdmin(GroupAdmin):
    form = GroupAdminForm


    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        school_id = request.POST['select_school']
        schoolObj = School.objects.filter(id=school_id)
        if schoolObj.first():
            schoolObj = schoolObj[0]
        else:
            schoolObj = None
        name = obj.name + '-' + get_initials_from_string(schoolObj.name)
        obj.name = name
        obj_save = super().save_model(request, obj, form, change)
        return obj_save
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        group_obj_list = super().get_queryset(request)
        if request.user.is_superuser:
            return group_obj_list
        else:
            if request.user.school:
                initals_name = '-' + get_initials_from_string(request.user.school.name)
                group_obj_list = group_obj_list.filter(name__icontains = initals_name)
                return group_obj_list
            else:
                return []
            
    
    def get_form(self, request, *args, **kwargs):
        form = super(GroupCustomAdmin, self).get_form(request, *args, **kwargs)
        form.request = request
        return form

