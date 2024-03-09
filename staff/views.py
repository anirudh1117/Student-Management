from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from utils.exceptions import InvalidUuidFormat
from trackActivity.mixins import ActivityLogMixin
from rest_framework.permissions import IsAuthenticated
from utils.permissions import MyPermission
from accounts.serializer import UserAccoutWriteSerializer

from .models import Department, Staff, StaffCustomField
from .serializer import DepartmentSerializer, StaffCustomFieldSerializer, StaffWriteSerializer
from .serializerRead import StaffSerializer

class DepartmentList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "staff.department"

    def get(self, request, format=None):
        departments = Department.objects.filter(school = request.user.school)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepartmentSerializer(data=request.data, context = {'request' : request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StaffList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "staff.staff"

    def get(self, request, format=None):
        staffList = Staff.objects.filter(account__school = request.user.school)
        serializer = StaffSerializer(staffList, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['role'] = 'staff'
        serializer = UserAccoutWriteSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            context = {
                "message" : "Email is send with username and password to the registered Staff"
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, id, format=None):
        request.POST['account'] = id
        serializer = StaffWriteSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            context = {
                "message" : "Account is added in Staff"
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)