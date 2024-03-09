from rest_framework import  serializers
from .models import Courses
from classes.models import Class
from utils.commonFunction import is_valid_uuid


class CoursesWriteSerializer(serializers.ModelSerializer):
    classID = serializers.CharField(required=False)
    className = serializers.CharField(required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        classID =  validated_data.pop('classID',None)
        className =  validated_data.pop('className',None)

        if classID is not None:
            if not is_valid_uuid(classID):
                raise serializers.ValidationError({"detail":"Not a valid Class Id!"})
            classObject = Class.objects.filter(id=classID, school = request.user.school)
            if classObject.first():
                classID = classObject[0]
            else:
                raise serializers.ValidationError({"detail":"Not a valid Class uuid!"})
        
        if className is not None:
            classObject = Class.objects.filter(name__iexact=className, school = request.user.school)
            if classObject.first():
                classID = classObject[0]
            else:
                raise serializers.ValidationError({"detail":"Not a valid Class Name!"})

        validated_data['classID'] = classID
        validated_data['school'] = request.user.school

        return Courses.objects.create(**validated_data)

    class Meta:
        model = Courses
        fields = '__all__'


class CoursesReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = '__all__'