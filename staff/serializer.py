from rest_framework import serializers

from .models import Department, Staff, StaffCustomField, Degree, Designation, StaffEducation, StaffPreviousExperience
from utils.commonFunction import convert_unix_time_millis_to_date


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


class DegreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Degree
        fields = '__all__'


class DesignationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['school'] = request.user.school

        return super().create(validated_data)

    class Meta:
        model = Designation
        exclude = ('school',)


class StaffEducationSerializer(serializers.ModelSerializer):
    start_date = serializers.CharField()
    end_date = serializers.CharField(required=False)
    degree = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context.get('request')
        start_date = validated_data.get("start_date", None)
        end_date = validated_data.get("end_date", None)
        degree_id = validated_data.get("degree", None)
        if start_date is not None:
            validated_data['start_date'] = convert_unix_time_millis_to_date(
                start_date)

        if end_date is not None:
            validated_data['end_date'] = convert_unix_time_millis_to_date(
                end_date)
        if degree_id is not None:
            degree = Degree.objects.filter(id=degree_id)
            if degree.first():
                validated_data['degree'] = degree[0]
            else:
                raise serializers.ValidationError(
                    {"detail": "Not a valid Degree ID!"})
        validated_data['school'] = request.user.school

        return super().create(validated_data)

    class Meta:
        model = StaffEducation
        fields = '__all__'


class PreviousExperienceSerializer(serializers.ModelSerializer):
    start_date = serializers.CharField()
    end_date = serializers.CharField(required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        start_date = validated_data.get("start_date", None)
        end_date = validated_data.get("end_date", None)
        if start_date is not None:
            validated_data['start_date'] = convert_unix_time_millis_to_date(
                start_date)

        if end_date is not None:
            validated_data['end_date'] = convert_unix_time_millis_to_date(
                end_date)
        validated_data['school'] = request.user.school

        return super().create(validated_data)

    class Meta:
        model = StaffPreviousExperience
        fields = '__all__'


class StaffCustomFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffCustomField
        fields = '__all__'


class StaffWriteSerializer(serializers.ModelSerializer):
    department = serializers.CharField()
    manager = serializers.CharField(required=False)
    joining_date = serializers.CharField(required=False)
    customFields = serializers.ListSerializer(
        child=serializers.JSONField(required=False), required=False)
    staffEducation = serializers.ListSerializer(
        child=StaffEducationSerializer(required=False), required=False)
    staffPreviousExperience = serializers.ListSerializer(
        child=PreviousExperienceSerializer(required=False), required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        department = validated_data.pop('department', None)
        manager = validated_data.pop('manager', None)
        staffEducation = validated_data.pop('staffEducation', [])
        staffPreviousExp = validated_data.pop('staffPreviousExperience', [])
        joiningDate = validated_data.pop('joining_date', None)

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

        if joiningDate is not None:
            validated_data['joining_date'] = convert_unix_time_millis_to_date(
                joiningDate)

        validated_data['department'] = department
        validated_data['manager'] = manager

        staff = super().create(validated_data)

        for staffEdu in staffEducation:
            staffEdu['staff'] = staff.employee_id
            staffEdu_serializer = StaffEducationSerializer(
                data=staffEdu, context={'request': request})
            if staffEdu_serializer.is_valid(raise_exception=True):
                staffEdu_serializer.save()
            else:
                print(staffEdu_serializer.error)
                raise serializers.ValidationError(staffEdu_serializer.errors)

        for staffPrevExp in staffPreviousExp:
            staffPrevExp['staff'] = staff.employee_id
            staffPrevExp_serializer = PreviousExperienceSerializer(
                data=staffPrevExp, context={'request': request})
            if staffPrevExp_serializer.is_valid(raise_exception=True):
                staffPrevExp_serializer.save()
            else:
                raise serializers.ValidationError(
                    staffPrevExp_serializer.errors)

        return staff

    class Meta:
        model = Staff
        fields = '__all__'
