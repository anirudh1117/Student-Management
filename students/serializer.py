from rest_framework import  serializers
from .models import Student, Guardian
from utils.commonFunction import is_valid_uuid
from classes.models import Class, Section



class StudentWriteSerializer(serializers.ModelSerializer):
    className = serializers.CharField(required=False)
    sectionName = serializers.CharField(required=False)
    classID = serializers.CharField(required=False)
    sectionID = serializers.CharField(required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        className =  validated_data.pop('className',None)
        sectionName =  validated_data.pop('sectionName',None)
        studentClass =  validated_data.pop('classID',None)
        section =  validated_data.pop('sectionID',None)

        print(studentClass)
        if studentClass is not None:
            
            print('heree')
            if not is_valid_uuid(studentClass):
                raise serializers.ValidationError({"detail":"Not a valid Class Id!"})
            classObject = Class.objects.filter(id=studentClass, school = request.user.school)
            if classObject.first():
                studentClass = classObject[0]
            else:
                raise serializers.ValidationError({"detail":"Not a valid Class uuid!"})

        if section is not None and is_valid_uuid(section):
            if not is_valid_uuid(section):
                raise serializers.ValidationError({"detail":"Not a valid Section Id!"})
            sectionObject = Section.objects.filter(id=section, school = request.user.school)
            if sectionObject.first():
                section = sectionObject[0]
            else:
                raise serializers.ValidationError({"detail":"Not a valid Section uuid!"})

        if className is not None:
            classObject = Class.objects.filter(name__iexact=className, school = request.user.school)
            if classObject.first():
                studentClass = classObject[0]
            else:
                raise serializers.ValidationError({"detail":"Not a valid Class Name!"})

        if sectionName is not None:
            sectionObject = Section.objects.filter(name__iexact=sectionName, school = request.user.school)
            if sectionObject.first():
                section = sectionObject[0]
            else:
                raise serializers.ValidationError({"detail":"Not a valid Section Name!"})
                
        validated_data['studentClass'] = studentClass
        validated_data['section'] = section
        
        student = Student.objects.create(**validated_data)
        return student

    class Meta:
        model = Student
        fields = '__all__'


class GuardianWriteSerializer(serializers.ModelSerializer):
    student = serializers.CharField(required=True)
    relationship = serializers.CharField(required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        student =  validated_data.pop('student',None)
        if student is None:
            raise serializers.ValidationError({"detail":"Not a valid Student Admission Number!"})
        else:
            studentObj = Student.objects.filter(admissionNumber=student, account__school = request.user.school)
            if studentObj.first():
                student = studentObj[0]
            else:
                raise serializers.ValidationError({"detail":"Not a valid Student Admission Number!"})
        validated_data['student'] = student
        guardian = Guardian.objects.create(**validated_data)
        return guardian

    class Meta:
        model = Guardian
        fields = '__all__'

