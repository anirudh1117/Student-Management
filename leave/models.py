from django.db import models
from rest_framework import serializers
from datetime import timedelta

from utils.commonFunction import slugify, get_Choices, common_error_message
from attendance.models import Holiday
from accounts.models import UserAccount
from school.models import Session
from utils import constants

class LeaveType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    total = models.PositiveIntegerField()
    name_slug = models.SlugField(blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL,  null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_slug
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
            leaveType = LeaveType.objects.filter(name_slug=self.name_slug, session = self.session)
            if leaveType.first():
                raise serializers.ValidationError({"detail" : "This leave type is already created"})
        super().save(*args, **kwargs)
 

class Leave(models.Model):
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    leave_Type = models.ForeignKey(LeaveType, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=False)
    status = models.CharField(max_length=10, choices=get_Choices(constants.Leave_Status), default='PENDING')
    session = models.ForeignKey(Session, on_delete=models.SET_NULL,  null=True)
    tagged_people = models.ManyToManyField(UserAccount, blank=True, related_name='tagged')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account} - {self.start_date} to {self.end_date}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs) -> None:
        self.holiday = Holiday.objects.values('date').all()
        super().__init__(*args, **kwargs)

    def get_total_leave_days(self):
        days = (self.end_date - self.start_date).days + 1
        for i in range(days):
            current_date = self.start_date + timedelta(days=i)
            if current_date.weekday() == 6 or current_date in self.holiday:
                days -= 1
        return days