from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from classes.models import Class
from subjects.models import Courses
from students.models import Student
from school.models import Session


class CourseSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseID =  models.ForeignKey(Courses, on_delete=models.DO_NOTHING, null=True)
    totalMarks = models.CharField(blank=True, max_length=5, null=True)
    startDateAndTime = models.DateTimeField(null=True)
    endDateAndTime = models.DateTimeField(null=True)
    description = models.TextField(blank=True, max_length=200, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    classes =  models.ForeignKey(Class, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, max_length=200, null=True)
    courses = models.ManyToManyField(CourseSchedule)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

class Marks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    examID =  models.ForeignKey(Exam, on_delete=models.CASCADE)
    CourseScheduleID =  models.ForeignKey(CourseSchedule, on_delete=models.DO_NOTHING)
    studentID =  models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True, max_length=200, null=True)

    MARKS_TYPE_CHOICES = (
        ('MARKS', 'Marks'),
        ('GRADE', 'Grade'),
        ('PERCENTAGE', 'Percentage'),
    )

    marksType = models.CharField(choices=MARKS_TYPE_CHOICES,blank=True, max_length=20, null=True)
    marks = models.CharField(blank=True, max_length=5, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


