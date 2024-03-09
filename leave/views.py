from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404
from utils.commonFunction import is_valid_uuid,string_to_uuid
from utils.exceptions import InvalidUuidFormat
from utils.permissions import MyPermission
from trackActivity.mixins import ActivityLogMixin

from .models import Leave, LeaveType
from .serializer import LeaveTypeSerializer, LeaveReadSerializer, LeaveWriteSerializer


# Create your views here.
class LeaveTypeList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "leave.leavetype"

    def get(self, request, format=None):
        leaves_type = LeaveType.objects.filter(session = request.user.school.current_session, session__school = request.user.school)
        serializer = LeaveTypeSerializer(leaves_type, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LeaveTypeSerializer(data=request.data, context = { 'request' : request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LeaveList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "leave.leave"

    def get(self, request, format=None):
        leaves = Leave.objects.filter(session = request.user.school.current_session, session__school = request.user.school)
        serializer = LeaveReadSerializer(leaves, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LeaveWriteSerializer(data=request.data, context = { 'request' : request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)