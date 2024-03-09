from django.db import models
from accounts.models import UserAccount
from rest_framework import serializers
import uuid

from school.models import Session
from utils.commonFunction import get_Choices
from utils import constants


class Holiday(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(unique=True)
    holiday_name = models.CharField(max_length=200)
    holiday_description = models.TextField(null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def save(self, *args, **kwargs):
        is_holiday = Holiday.objects.filter(date=self.date).first()
        if is_holiday:
            raise serializers.ValidationError(
                { "detail" : "A holiday already exists with the same date."})
        super().save(*args, **kwargs)


class StudentAttendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField() 
    student = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    staff = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='staff_attendance')
    status = models.CharField(blank=True, max_length=20, null=True, choices=get_Choices(constants.Attendance_List))
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        unique_together = ('date', 'student', 'staff')

    def save(self, *args, **kwargs):
        is_holiday = Holiday.objects.filter(date=self.date.strftime('%Y-%m-%d')).first()
        existing_attendance = StudentAttendance.objects.filter(date=self.date.strftime('%Y-%m-%d'), student=self.student)
        if is_holiday:
            raise serializers.ValidationError(
                { "detail" : "Today is marked as holiday, Attendance cannot be marked on a Holiday"})
        elif self.date.weekday() == 5:  # 6 represents Sunday
            raise serializers.ValidationError({ "detail" :
                'Attendance cannot be marked on a Sunday'})
        elif existing_attendance.first():
             existing_attendance.update(status=self.status, staff=self.staff)
             return existing_attendance
        super().save(*args, **kwargs)
