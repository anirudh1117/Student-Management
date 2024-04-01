from rest_framework import serializers

from accounts.serializer import UserAccountReadSerializer
from staff.serializerRead import StaffTeacherSerializer, StaffEducationReadSerializer, StaffPreviousExperienceReadSerializer
from .models import Teacher


class TeacherWriteSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context.get('request')

        return super().create(validated_data)

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherReadSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()
    staff = serializers.SerializerMethodField()
    teacherEducation = serializers.SerializerMethodField()
    teacherExperience = serializers.SerializerMethodField()

    def get_account(self, teacherObj):
        userObj = teacherObj.staff.account
        serializer = UserAccountReadSerializer(userObj, context=self.context)
        return serializer.data

    def get_staff(self, teacherObj):
        staffObj = teacherObj.staff
        serializer = StaffTeacherSerializer(staffObj, context=self.context)
        return serializer.data

    def get_teacherEducation(self, teacherObj):
        teacherEducation = teacherObj.staff.education.all()
        serializer = StaffEducationReadSerializer(
            teacherEducation, many=True, context=self.context)
        return serializer.data
    
    def get_teacherExperience(self, teacherObj):
        teacherExperience = teacherObj.staff.experiences.all()
        serializer = StaffPreviousExperienceReadSerializer(
            teacherExperience, many=True, context=self.context)
        return serializer.data

    def create(self, validated_data):
        request = self.context.get('request')

        return super().create(validated_data)

    class Meta:
        model = Teacher
        fields = '__all__'
