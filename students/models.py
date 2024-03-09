from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import UserAccount
from classes.models import Section, Class

class Student(models.Model):
    admissionNumber = models.AutoField(primary_key=True)
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    section =  models.ForeignKey(Section, on_delete=models.DO_NOTHING,blank=True, null=True)
    studentClass =  models.ForeignKey(Class, on_delete=models.DO_NOTHING,blank=True, null=True)

    def __str__(self):
        return str(self.admissionNumber)



class Guardian(models.Model):
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    relationship = models.CharField(blank=True, max_length=20, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
