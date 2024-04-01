import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from school.models import School

class Class(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'),blank=True, max_length=1000)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)



class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    classID =  models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=100)
    description = models.CharField(_('Description'),blank=True, max_length=100)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.classID.name + self.name

