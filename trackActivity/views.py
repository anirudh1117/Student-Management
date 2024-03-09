from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ActivityLog
from .serializer import LogActivitySerializer
from utils.permissions import MyPermission

# Create your views here.

class ActivityLogList(APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "trackactivity.activitylog"

    def get(self, request, format=None):
        activityLog = ActivityLog.objects.all()
        serializer = LogActivitySerializer(activityLog, many=True)
        return Response(serializer.data)
