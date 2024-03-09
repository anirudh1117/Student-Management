from rest_framework import serializers
import calendar
from datetime import timedelta, datetime

from .models import Holiday, StudentAttendance
from accounts.models import UserAccount
from students.models import Student
from utils.commonFunction import convert_unix_time_millis_to_date_time
from utils.constants import Attendance_List, Attendance_Type

class HolidaySerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()

    def get_day(self,obj):
        if obj:
            return calendar.day_name[obj.date.weekday()]
        return ''

    class Meta:
        model = Holiday
        fields = '__all__'



class HolidayWriteSerializer(serializers.ModelSerializer):
    date = serializers.CharField(required=True)

    def create(self, validated_data):
        request = self.context.get('request')
        date = validated_data.pop('date',None)
        date = convert_unix_time_millis_to_date_time(date)
        validated_data['date'] = date
        validated_data['session'] = request.user.school.current_session
        return Holiday.objects.create(**validated_data)

    class Meta:
        model = Holiday
        fields = '__all__'


class StudentAttendanceSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()

    def get_day(self,obj):
        if obj:
            return calendar.day_name[obj.date.weekday()]
        return ''
 
    class Meta:
        model = StudentAttendance
        fields = '__all__'


class StudentAttendanceWriteSerializer(serializers.ModelSerializer):
    student = serializers.CharField(required=False)
    students = serializers.ListSerializer(child=serializers.CharField(),required=False)
    classId = serializers.CharField(required=False)

    def create(self, validated_data):
        request = self.context['request']
        self.type = request.query_params.get('type').lower()
        self.status = request.query_params.get('status').upper()

        if not type or len(self.type) == 0 or not self.status or len(self.status) == 0:
            raise serializers.ValidationError({"detail" : "type and status is mandatory query params."})
        elif not (self.status in Attendance_List):
            raise serializers.ValidationError({"detail" : "Choices for status is : " + ", ".join(Attendance_List)})
        elif not (self.type in Attendance_Type):
            raise serializers.ValidationError({"detail" : "Choices for type is : " + ", ".join(Attendance_Type)})
        if self.type == 'single':
            id = validated_data.pop('student')
            create_data = self.get_validatedData(request, self.get_UserAccount(id))
            attendance  = StudentAttendance.objects.create(**create_data)
        
        elif self.type == 'list':
            students_list = validated_data.pop('students')
            for id in students_list:
                create_data = self.get_validatedData(request, self.get_UserAccount(id))
                attendance  = StudentAttendance.objects.create(**create_data)
        
        elif self.type == 'class':
            id = validated_data.pop('classId')
            studentObj = Student.objects.filter(studentClass=id)
            for student in studentObj:
                create_data = self.get_validatedData(request, student.account)
                attendance  = StudentAttendance.objects.create(**create_data)

        return {"detail" : "Success"}
    
    def get_UserAccount(self, id):
        return UserAccount.objects.get(id=id)
    
    def get_validatedData(self, request, userAccount):
        validated_data = {}
        validated_data['staff'] = request.user
        validated_data['date'] = datetime.now()
        validated_data['status'] = self.status.upper()
        validated_data['student'] = userAccount
        validated_data['session'] = request.user.school.current_session
        return validated_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ''
        self.status = ''


    class Meta:
        model = StudentAttendance
        fields = ['student', 'students','classId']