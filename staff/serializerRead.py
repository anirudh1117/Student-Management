from rest_framework import serializers

from .models import Staff
from .serializer import DepartmentSerializer
from accounts.serializer import UserAccountReadSerializer

class StaffSerializer(serializers.ModelSerializer):
    account = UserAccountReadSerializer()
    department = DepartmentSerializer()
    reportee = serializers.SerializerMethodField()

    def get_reportee(self, obj):
        request = self.context.get("request")
        fields = request.query_params.get('fields', None)
        if fields:
            fields = fields.split(',')
            pass
        else:
            return []

    class Meta:
        model = Staff
        fields = '__all__'