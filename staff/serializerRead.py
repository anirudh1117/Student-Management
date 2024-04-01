from rest_framework import serializers

from .models import Staff, StaffEducation, StaffPreviousExperience
from .serializer import DepartmentSerializer, DegreeSerializer, DesignationSerializer
from accounts.serializer import UserAccountReadSerializer
from utils.commonFunction import convert_date_time_to_unix_time_millis, convert_date_to_unix_time_millis


class StaffSerializer(serializers.ModelSerializer):
    account = UserAccountReadSerializer()
    department = DepartmentSerializer()
    reportee = serializers.SerializerMethodField()
    designation = DesignationSerializer()
    reportee = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    joining_date = serializers.SerializerMethodField()
    teacherEducation = serializers.SerializerMethodField()
    teacherExperience = serializers.SerializerMethodField()

    def get_reportee(self, obj):
        request = self.context.get("request")
        fields = request.query_params.get('fields', None)
        if fields:
            fields = fields.split(',')
            pass
        else:
            return []
        
    def get_reportee(self, obj):
        request = self.context.get("request")
        fields = request.query_params.get('fields', None)
        if fields:
            fields = fields.split(',')
            pass
        else:
            return []
    
    def get_created_at(self, staffEduObj):
        if staffEduObj.created_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(staffEduObj.created_at)

    def get_updated_at(self, staffEduObj):
        if staffEduObj.updated_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(staffEduObj.updated_at)
    
    def get_joining_date(self, staffEduObj):
        if staffEduObj.joining_date is None:
            return ""
        return convert_date_to_unix_time_millis(staffEduObj.joining_date)
    
    def get_teacherEducation(self, staffObj):
        teacherEducation = staffObj.education.all()
        serializer = StaffEducationReadSerializer(
            teacherEducation, many=True, context=self.context)
        return serializer.data
    
    def get_teacherExperience(self, staffObj):
        teacherExperience = staffObj.experiences.all()
        serializer = StaffPreviousExperienceReadSerializer(
            teacherExperience, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Staff
        fields = '__all__'

class StaffTeacherSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    designation = DesignationSerializer()
    reportee = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    joining_date = serializers.SerializerMethodField()

    def get_reportee(self, obj):
        request = self.context.get("request")
        fields = request.query_params.get('fields', None)
        if fields:
            fields = fields.split(',')
            pass
        else:
            return []
    
    def get_created_at(self, staffEduObj):
        if staffEduObj.created_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(staffEduObj.created_at)

    def get_updated_at(self, staffEduObj):
        if staffEduObj.updated_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(staffEduObj.updated_at)
    
    def get_joining_date(self, staffEduObj):
        if staffEduObj.joining_date is None:
            return ""
        return convert_date_to_unix_time_millis(staffEduObj.joining_date)


    class Meta:
        model = Staff
        fields = '__all__'



class StaffEducationReadSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    degree = DegreeSerializer()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_start_date(self, staffEduObj):
        if staffEduObj.start_date is None:
            return ""
        return convert_date_to_unix_time_millis(staffEduObj.start_date)

    def get_end_date(self, staffEduObj):
        if staffEduObj.end_date is None:
            return ""
        return convert_date_to_unix_time_millis(staffEduObj.end_date)

    def get_created_at(self, staffEduObj):
        if staffEduObj.created_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(staffEduObj.created_at)

    def get_updated_at(self, staffEduObj):
        if staffEduObj.updated_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(staffEduObj.updated_at)

    class Meta:
        model = StaffEducation
        fields = '__all__'


class StaffPreviousExperienceReadSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_start_date(self, staffPrevExpObj):
        if staffPrevExpObj.start_date is None:
            return ""
        return convert_date_to_unix_time_millis(staffPrevExpObj.start_date)

    def get_end_date(self, staffPrevExpObj):
        if staffPrevExpObj.end_date is None:
            return ""
        return convert_date_to_unix_time_millis(staffPrevExpObj.end_date)

    def get_created_at(self, staffPrevExpObj):
        if staffPrevExpObj.created_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(staffPrevExpObj.created_at)

    def get_updated_at(self, staffPrevExpObj):
        if staffPrevExpObj.updated_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(staffPrevExpObj.updated_at)

    class Meta:
        model = StaffPreviousExperience
        fields = '__all__'
