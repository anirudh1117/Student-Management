from django.contrib import admin
from typing import Any
from django import forms
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import School, Session
from utils.commonFunction import get_school_list

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['registerationnumber', 'name','city', 'state', 'country', 'current_session']
    ordering = ['-country', '-state', '-city', '-name']
    list_filter = ['country','city']

class SessionAdminForm(forms.ModelForm):
    select_school = forms.ChoiceField(required=True, choices=get_school_list())

    def __init__(self, *args, **kwargs):
        super(SessionAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['select_school'].initial = instance.school.id

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['school', 'name','start_date', 'end_date', 'is_current']
    exclude = ('school',)
    ordering = ['-start_date']
    form = SessionAdminForm

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        school_id = request.POST['select_school']
        schoolObj = School.objects.filter(id=school_id)
        if schoolObj.first():
            schoolObj = schoolObj[0]
        else:
            schoolObj = None
        obj.school = schoolObj
        obj_save = super().save_model(request, obj, form, change)
        if obj.is_current:
            session_obj = Session.objects.filter(school = obj.school).filter(is_current = True).exclude(id = obj.id)
            if session_obj.first():
                for session in session_obj:
                    session.is_current = False
                    session.save()
            schoolObj.current_session = obj
            schoolObj.save()
        return obj_save
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        session_obj_list = super().get_queryset(request)
        if request.user.is_superuser:
            return session_obj_list
        else:
            if request.user.school:
                session_obj_list = session_obj_list.filter(school = request.user.school)
                return session_obj_list
            else:
                return []
