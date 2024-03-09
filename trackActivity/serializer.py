from rest_framework import  serializers
from .models import ActivityLog

class LogActivitySerializer(serializers.ModelSerializer):


    class Meta:
        model = ActivityLog
        fields = '__all__'