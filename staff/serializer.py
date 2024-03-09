from rest_framework import serializers

from .models import Department, Staff, StaffCustomField
from utils.commonFunction import string_to_uuid


class DepartmentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context.get("request")
        name = validated_data.get('name', None)
        is_Department = Department.objects.filter(
            name__iexact=name, school=request.user.school)
        if is_Department.first():
            raise serializers.ValidationError(
                {"detail": "Department already exists with the same name."})
        validated_data['school'] = request.user.school

        return super().create(validated_data)

    class Meta:
        model = Department
        fields = '__all__'


class StaffCustomFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffCustomField
        fields = '__all__'


class StaffWriteSerializer(serializers.ModelSerializer):
    department = serializers.CharField(required=False)
    manager = serializers.CharField(required=False)
    customFields = serializers.ListSerializer(
        child=serializers.JSONField(required=False), required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        department = validated_data.pop('department', None)
        manager = validated_data.pop('manager', None)

        if department is not None:
            departmentObj = Department.objects.filter(
                id=department, school=request.user.school)
            if departmentObj.first():
                department = departmentObj[0]
            else:
                raise serializers.ValidationError(
                    {"detail": "Not a valid Department uuid!"})

        if manager is not None:
            managerObj = Staff.objects.filter(
                employee_id=manager, account__school=request.user.school)
            if managerObj.first():
                manager = managerObj[0]
            else:
                raise serializers.ValidationError(
                    {"detail": "Not a valid Manager!"})

        validated_data['department'] = department
        validated_data['manager'] = manager

        return super().create(validated_data)

    class Meta:
        model = Staff
        fields = '__all__'
