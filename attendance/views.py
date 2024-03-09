from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from utils.commonFunction import convert_unix_time_millis_to_date_time
from utils.exceptions import InvalidUuidFormat
from trackActivity.mixins import ActivityLogMixin
from rest_framework.permissions import IsAuthenticated
from utils.permissions import MyPermission

from .serializer import HolidaySerializer, HolidayWriteSerializer, StudentAttendanceSerializer, StudentAttendanceWriteSerializer
from .models import Holiday, StudentAttendance
from students.models import Student


class HoldiaysList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "attendance.holiday"

    def get(self, request, format=None):
        holidays = Holiday.objects.filter(session__school = request.user.school, session = request.user.school.current_session)
        serializer = HolidaySerializer(holidays, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HolidayWriteSerializer(data=request.data, context = {'request' : request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentAttendanceList(ActivityLogMixin,APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "attendance.studentattendance"

    def get(self, request, format=None):
        attendance = StudentAttendance.objects.filter(session__school = request.user.school, session = request.user.school.current_session)
        attendance = self.filter_attendance(attendance, request.GET)
        serializer = StudentAttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentAttendanceWriteSerializer(data=request.data, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res = {
                "detail" : "success"
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def filter_attendance(self, attendance, params):
        for key, value in params.items():
            if len(value) == 0:
                pass
            elif key == 'status':
                attendance = attendance.filter(status=value.upper())
            elif key == 'class':
                accountList = []
                studentsInClass = Student.objects.filter(studentClass=value)
                for student in studentsInClass:
                    accountList.append(student.account)
                attendance = attendance.filter(student__in=accountList)
            elif key == 'student':
                attendance = attendance.filter(student=value)
            elif key == 'staff':
                attendance = attendance.filter(staff=value)
            elif key == 'date':
                dateAndTime = convert_unix_time_millis_to_date_time(value)
                attendance = attendance.filter(date=dateAndTime.strftime('%Y-%m-%d'))
            elif key == 'startDate':
                dateAndTime = convert_unix_time_millis_to_date_time(value)
                attendance = attendance.filter(date__gte=dateAndTime.strftime('%Y-%m-%d'))
            elif key == 'endDate':
                dateAndTime = convert_unix_time_millis_to_date_time(value)
                attendance = attendance.filter(date__lte=dateAndTime.strftime('%Y-%m-%d'))

        return attendance 


