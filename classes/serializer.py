from rest_framework import  serializers
from .models import Class, Section
from utils.commonFunction import string_to_uuid,convert_date_time_to_unix_time_millis, common_error_message
from subjects.models import Courses
from subjects.serializer import CoursesReadSerializer

class ClassSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context.get('request')
        name = validated_data.get('name', None)
        validated_data['school'] = request.user.school
        if name:
            classObj = Class.objects.filter(name__iexact = name, school = request.user.school)
            if classObj.first():
                raise serializers.ValidationError(common_error_message("Class with Same name is already created!."))
        print(validated_data)
        return Class.objects.create(**validated_data)

    def update(self, instance, validated_data):
        id = string_to_uuid(instance.id)
        Class.objects.filter(id=id).update(**validated_data)

    class Meta:
        model = Class
        fields = '__all__'

class ClassReadSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    sections = serializers.SerializerMethodField()

    def get_created_at(self,obj):
        if obj.created_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(obj.created_at)
    
    def get_updated_at(self,obj):
        if obj.updated_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(obj.updated_at)

    def get_courses(self,obj):
        if obj is None:
            return []
        coursesObject = Courses.objects.filter(classID=obj)
        if coursesObject.first():
            return CoursesReadSerializer(coursesObject,many=True).data
        return []
    
    def get_sections(self,obj):
        if obj is None:
            return []
        sectionObject = Section.objects.filter(classID=obj.id)
        if sectionObject.first():
            return SectionSerializer(sectionObject,many=True).data
        return []

    class Meta:
        model = Class
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
   classID = serializers.CharField(required=False)
    
   def create(self, validated_data):
        request = self.context.get('request')
        validated_data['school'] = request.user.school
        id = string_to_uuid(request.parser_context.get('kwargs').get('id'))
        classObject = Class.objects.filter(id=id, school = request.user.school)
        if classObject.first():
            classObject = classObject[0]
        else:
            raise serializers.ValidationError(common_error_message("This Class is not registered with your School!."))
        print(classObject)
        validated_data['classID'] = classObject
        print(validated_data)
        return Section.objects.create(**validated_data)

   def update(self, instance, validated_data):
        id = string_to_uuid(instance.id)
        Section.objects.filter(id=id).update(**validated_data)

   class Meta:
        model = Section
        fields = '__all__'