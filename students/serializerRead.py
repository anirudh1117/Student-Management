from rest_framework import  serializers
from accounts.serializer import UserAccountReadSerializer
from .models import Student, Guardian


class StudentReadSerializer(serializers.ModelSerializer):
    roll_no = serializers.SerializerMethodField()
    account  = UserAccountReadSerializer()
    studentClass = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
    guardian = serializers.SerializerMethodField()
    

    def get_studentClass(self,obj):
        if obj.studentClass is not None:
            return obj.studentClass.name
        return ''

    def get_section(self,obj):
        if obj.section is not None:
            return obj.section.name
        return ''
    
    def get_guardian(self,obj):
        guardianObj = Guardian.objects.filter(student=obj)
        if guardianObj.first():
            return GuardianReadSerializer(guardianObj,many=True).data
        return []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.roll_no_counters = {}

    def get_roll_no(self, obj):
        class_name = obj.studentClass
        if class_name not in self.roll_no_counters:
            self.roll_no_counters[class_name] = 1
        roll_no = self.roll_no_counters[class_name]
        self.roll_no_counters[class_name] += 1
        return str(roll_no)

    class Meta:
        model = Student
        fields = '__all__'


class GuardianReadSerializer(serializers.ModelSerializer):
    account  = UserAccountReadSerializer()

    class Meta:
        model = Guardian
        fields = '__all__'