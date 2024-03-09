from rest_framework import  serializers
from .models import Exam, CourseSchedule, Marks
from classes.serializer import ClassReadSerializer
from subjects.serializer import CoursesReadSerializer
from utils.commonFunction import convert_date_time_to_unix_time_millis,string_to_uuid, is_valid_uuid, common_error_message
from subjects.models import Courses
from classes.models import Class
from students.models import Student


class CourseScheduleReadSerializer(serializers.ModelSerializer):
    courseID = CoursesReadSerializer()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self,obj):
        if obj.created_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(obj.created_at)
    
    def get_updated_at(self,obj):
        if obj.updated_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(obj.updated_at)

    class Meta:
        model = CourseSchedule
        fields = '__all__'

class ExamReadSerializer(serializers.ModelSerializer):
    classes = ClassReadSerializer()
    courses = CourseScheduleReadSerializer(many=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    #marksType = serializers.CharField(source='get_marksType_display')

    def get_created_at(self,obj):
        if obj.created_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(obj.created_at)
    
    def get_updated_at(self,obj):
        if obj.updated_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(obj.updated_at)


    class Meta:
        model = Exam
        fields = '__all__'

class MarksReadSerializer(serializers.ModelSerializer):
    CourseScheduleID = CourseScheduleReadSerializer()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self,obj):
        if obj.created_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(obj.created_at)
    
    def get_updated_at(self,obj):
        if obj.updated_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(obj.updated_at)


    class Meta:
        model = Marks
        fields = '__all__'


class CourseScheduleWriteSerializer(serializers.ModelSerializer):
    courseID = serializers.CharField()

    def create(self, validated_data):
        request = self.context.get('request')
        school = request.user.school
        session = validated_data.get('session', None)
        courseID =  validated_data.get('courseID',None)
        id = string_to_uuid(request.parser_context.get('kwargs').get('id'))

        if courseID is not None and is_valid_uuid(courseID):
            courseObject = Courses.objects.filter(id=courseID, school = school)
            if courseObject.first():
                courseID = courseObject[0]
            else:
                print(courseID)
                raise serializers.ValidationError(common_error_message("Not a valid Course id!"))
        else:
            raise serializers.ValidationError(common_error_message("Not a valid Course uuid!"))
        
        validated_data['courseID'] = courseID

        courseSchedule = CourseSchedule.objects.create(**validated_data)
        exams = Exam.objects.filter(id=id, session__school = school, session = session)
        if exams.first():
            for exam in exams:
                exam.courses.add(courseSchedule)
        else:
            serializers.ValidationError(common_error_message("Not a valid Exam!. Course is created but not added to exam"))
        return courseSchedule

    class Meta:
        model = CourseSchedule
        fields = '__all__'

class ExamWriteSerializer(serializers.ModelSerializer):
    courses = serializers.ListSerializer(child=CourseScheduleWriteSerializer(required=False),required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        courses =  validated_data.pop('courses',None)
        classId = validated_data.get('classes', None)

        if classId is not None and is_valid_uuid(classId.id):
            classObj = Class.objects.filter(id = classId.id, school = request.user.school)
            if classObj.first():
                pass
            else:
                raise serializers.ValidationError(common_error_message("Not a valid Class ID!"))
        else:
            raise serializers.ValidationError(common_error_message("Not a valid Class uuid!"))
        
        exams = Exam.objects.create(**validated_data)

        if courses is not None : 
            courses['session'] = request.user.school.current_session
            serializer = CourseScheduleWriteSerializer(data=courses,many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                json_data = serializer.data
                for i, val in enumerate(json_data):
                    for key,value in val.items():
                        if key == 'id':
                            exams.courses.add(value)
                            break              
                    #print(jsonData[i])
                #exams.courses.add(**serializer.data)
            else:
                raise serializers.ValidationError(serializer.errors)  
        return exams

    class Meta:
        model = Exam
        fields = '__all__'

class MarksWriteSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context.get('request')
        examId = validated_data.get('examID',None)
        CourseScheduleID = validated_data.get('CourseScheduleID', None)
        studentID = validated_data.get('studentID', None)
        session = validated_data.get('session', None)

        print(examId)

        if examId is not None and is_valid_uuid(examId.id):
            examObj = Exam.objects.filter(id=examId.id, session = session)
            if not examObj.first():
                serializers.ValidationError(common_error_message("Not a valid Exam id!"))
        else:
            raise serializers.ValidationError(common_error_message("Not a valid Exam uuid!"))
        

        if CourseScheduleID is not None and is_valid_uuid(CourseScheduleID.id):
            courseScheduleObj = CourseSchedule.objects.filter(id=CourseScheduleID.id, session = session)
            if not courseScheduleObj.first():
                serializers.ValidationError(common_error_message("Not a valid Course Schedule id!"))
        else:
            raise serializers.ValidationError(common_error_message("Not a valid Course Schedule uuid!"))
        

        if studentID is not None:
            studentObj = Student.objects.filter(admissionNumber=studentID.admissionNumber, account__school = request.user.school)
            if not studentObj.first():
                serializers.ValidationError(common_error_message("Not a valid Student id!"))
        else:
            raise serializers.ValidationError(common_error_message("Student ID is None!"))
        

        return Marks.objects.create(**validated_data)



    class Meta:
        model = Marks
        fields = '__all__'