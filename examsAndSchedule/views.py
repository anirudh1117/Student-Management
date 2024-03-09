from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from utils.commonFunction import is_valid_uuid
from utils.exceptions import InvalidUuidFormat
from trackActivity.mixins import ActivityLogMixin
from rest_framework.permissions import IsAuthenticated
from utils.permissions import MyPermission

from .serializer import ExamReadSerializer, ExamWriteSerializer, MarksWriteSerializer, MarksReadSerializer, CourseScheduleReadSerializer, CourseScheduleWriteSerializer
from .models import Exam, Marks


class ExamsList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "examsAndSchedule.exam"

    def get(self, request, format=None):
        exams = Exam.objects.filter(session__school = request.user.school)
        exams = filter_exams(exams, request)
        serializer = ExamReadSerializer(exams, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['session'] = request.user.school.current_session.id
        serializer = ExamWriteSerializer(data=request.data, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseScheduleList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "examsAndSchedule.courseschedule"

    def get(self, request, id, format=None):
        courses = []
        exams = Exam.objects.filter(id=id, session__school = request.user.school, session = request.user.school.current_session)
        for exam in exams:
            courses = exam.courses.all()
            print(exam.courses)
        serializer = CourseScheduleReadSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        request.data['session'] = request.user.school.current_session.id
        serializer = CourseScheduleWriteSerializer(
            data=request.data, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarksList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "examsAndSchedule.marks"

    def get(self, request, format=None):
        marks = Marks.objects.filter(session__school = request.user.school)
        marks = filter_marks(marks, request)
        serializer = MarksReadSerializer(marks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['session'] = request.user.school.current_session.id
        serializer = MarksWriteSerializer(data=request.data, context = {'request' : request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def filter_marks(marks, request):
    session = False
    for key, value in request.GET.items():
        if len(value) == 0:
            pass
        elif key == 'examID':
            if is_valid_uuid(value):
                marks = marks.filter(examID=value)
            else:
                raise InvalidUuidFormat()
        elif key == 'CourseScheduleID':
            if is_valid_uuid(value):
                marks = marks.filter(CourseScheduleID=value)
            else:
                raise InvalidUuidFormat()
        elif key == 'studentID':
            if is_valid_uuid(value):
                marks = marks.filter(studentID=value)
            else:
                raise InvalidUuidFormat()
        elif key == 'marks':
            marks = marks.filter(marks=value)
        elif key == 'marksLte':
            marks = marks.filter(marks__lte=value)
        elif key == 'marksGte':
            marks = marks.filter(marks__gte=value)
        elif key == 'session' : 
            marks = marks.filter(session=value)
            session = True
    
    if not session:
        marks = marks.filter(session = request.user.school.current_session)

    return marks

def filter_exams(exams, request):
    session = False
    for key, value in request.GET.items():
        if len(value) == 0:
            pass
        elif key == 'classes':
            if is_valid_uuid(value):
                exams = exams.filter(classes=value)
            else:
                raise InvalidUuidFormat()
        elif key == 'courses':
            print(key,value)
            if is_valid_uuid(value):
                exams = exams.filter(courses__id=value)
            else:
                raise InvalidUuidFormat()
        elif key == 'name':
            exams = exams.filter(name__icontains=value)
        elif key == 'session' : 
            exams = exams.filter(session=value)
            session = True

    if not session:
        exams = exams.filter(session = request.user.school.current_session)

    return exams
