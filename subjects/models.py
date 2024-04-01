from django.db import models
from django.utils.translation import gettext_lazy as _

from classes.models import Class
from school.models import School
import uuid

class Courses(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subjectID = models.CharField(max_length=20)
    classID =  models.ForeignKey(Class, on_delete=models.DO_NOTHING,blank=True, null=True)
    name = models.CharField(blank=True, max_length=20, null=True)
    bookName = models.CharField(blank=True, max_length=20, null=True)
    description = models.CharField(blank=True, max_length=1000, null=True)
    syllabus = models.ImageField(upload_to='subjects/%Y/', blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)