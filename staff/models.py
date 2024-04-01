import datetime
from django.db import models
import uuid

from accounts.models import UserAccount
from school.models import School


class Degree(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=20)
    prio = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.abbreviation} - {self.name}"

    class Meta:
        ordering = ['prio']


class Designation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    department_fields = models.JSONField(blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Staff(models.Model):
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    designation = models.ForeignKey(
        Designation, null=True, on_delete=models.DO_NOTHING)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    employee_id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    joining_date = models.DateField(blank=True, null=True)
    manager = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField('Description', blank=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StaffCustomField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StaffEducation(models.Model):
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name='education', null=True)
    institution_name = models.CharField(max_length=255)
    degree = models.ForeignKey(
        Degree, on_delete=models.CASCADE, related_name='educations')
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    documents = models.FileField(
        upload_to='education_documents/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return f"{self.degree.abbreviation} in {self.field_of_study} from {self.institution_name}"


class StaffPreviousExperience(models.Model):
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name='experiences', null=True)
    organization_name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    # Allows for ongoing positions
    end_date = models.DateField(null=True, blank=True)
    # Optional detailed description
    description = models.TextField(blank=True, null=True)
    documents = models.FileField(
        upload_to='experience_documents/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return f"{self.position} at {self.organization_name}"
