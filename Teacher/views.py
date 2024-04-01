from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from schoolARP.customPagination import CustomPageNumberPagination
from staff.serializer import StaffWriteSerializer
from utils.exceptions import InvalidUuidFormat
from trackActivity.mixins import ActivityLogMixin
from rest_framework.permissions import IsAuthenticated
from utils.permissions import MyPermission
from utils.constants import STAFF
from accounts.serializer import UserAccoutWriteSerializer

from .models import Teacher
from .serializer import TeacherWriteSerializer, TeacherReadSerializer


class TeacherList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "Teacher.teacher"

    def get(self, request, format=None):
        teacherList = Teacher.objects.filter(school=request.user.school)
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(teacherList, request)

        if page is not None:
            serializer = TeacherReadSerializer(
            page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = TeacherReadSerializer(
            teacherList, many=True, context={"request": request})
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, format=None):
        request.data['role'] = STAFF
        request.data['school'] = request.user.school.id

        account_serializer = UserAccoutWriteSerializer(
            data=request.data, context={"request": request})
        if account_serializer.is_valid(raise_exception=True):
            account = account_serializer.save()
            request.data['account'] = account.id

            staff_serializer = StaffWriteSerializer(
                data=request.data, context={"request": request})
            if staff_serializer.is_valid(raise_exception=True):
                staff = staff_serializer.save()
                request.data['staff'] = staff.employee_id
                teacher_serializer = TeacherWriteSerializer(
                    data=request.data, context={"request": request})
                if teacher_serializer.is_valid(raise_exception=True):
                    teacher_serializer.save()
                    context = {
                        "message": "Email is send with username and password to the registered Staff"
                    }
                    return Response(context, status=status.HTTP_201_CREATED)
                else:
                    return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(staff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
