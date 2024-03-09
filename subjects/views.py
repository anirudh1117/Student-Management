from utils.permissions import MyPermission
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from .models import Courses
from .serializer import CoursesReadSerializer, CoursesWriteSerializer
from trackActivity.mixins import ActivityLogMixin


class CoursesList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "subjects.courses"

    def get(self, request, format=None):
        courses = Courses.objects.filter(school=request.user.school)
        serializer = CoursesReadSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CoursesWriteSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
