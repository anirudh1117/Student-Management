from utils.permissions import MyPermission
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from .models import Student, Guardian
from .serializerRead import StudentReadSerializer, GuardianReadSerializer
from accounts.serializer import UserAccoutWriteSerializer
from trackActivity.mixins import ActivityLogMixin



class StudentList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "students.student"

    def get(self, request, format=None):
        students = Student.objects.filter(account__school = request.user.school).order_by('account__first_name','account__middle_name','account__last_name')
        serializer = StudentReadSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['role'] = 'student'
        serializer = UserAccoutWriteSerializer(data=request.data, context = {'request' : request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            context = {
                "message" : "Email is send with username and password to the registered Student"
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuardianList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "students.guardian"

    def get(self, request, format=None):
        guardians = Guardian.objects.filter(account__school = request.user.school)
        serializer = GuardianReadSerializer(guardians, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['role'] = 'guardian'
        serializer = UserAccoutWriteSerializer(data=request.data, context = {'request' : request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            context = {
                "message" : "Email is send with username and password to the registered Guardian"
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)