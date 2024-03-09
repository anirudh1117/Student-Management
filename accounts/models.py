from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from rest_framework import serializers

from .managers import CustomUserManager
from utils import constants
from utils.commonFunction import get_Choices, common_error_message
from school.models import School


class UserAccount(AbstractUser, PermissionsMixin):
    username = None
    email = models.CharField(_('email address'), unique=True, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    ROLE_CHOICES = (
        ('useradmin', 'User Admin'),
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('guardian', 'Guardian')
    )

    first_name = models.CharField(_('first name'), blank=True, max_length=100)
    middle_name = models.CharField(
        _('middle name'), blank=True, max_length=100)
    last_name = models.CharField(_('last name'), blank=True, max_length=100)
    date_of_birth = models.DateField(null=True)
    phoneNo = models.CharField(
        _('phone No.'), blank=True, max_length=10, null=True)
    bloodGroup = models.CharField(
        _('Blood Group'), blank=True, max_length=5, null=True)
    role = models.CharField(_('role'), blank=True, max_length=20,
                            null=True, choices=get_Choices(constants.Role_Choices))
    profileLogo = models.ImageField(
        upload_to='photos/accounts/%Y/%m/%d/', blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # def __str__(self):
    # return self.first_name + ' ' + self.last_name + '( ' + self.role +  ', ' + self.date_of_birth +' )'

    def save(self, *args, **kwargs):
        if self.id is None and self.email:
            try:
                validate_email(self.email)
            except:
                raise serializers.ValidationError(
                    common_error_message("Email is not valid!"))

            account = UserAccount.objects.filter(email__iexact=self.email)
            if account.first():
                raise serializers.ValidationError(common_error_message(
                    self.email + " is already linked with different user."))
        else:
            pass
            #self.school = School.objects.filter(id=self.school)[0]
    
        super().save(*args, **kwargs)


class Address(models.Model):
    account = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, default=None)
    line1 = models.CharField(_('line1'), blank=True, max_length=150)
    line2 = models.CharField(_('line2'), blank=True, max_length=150)
    city = models.CharField(_('city'), max_length=300)
    zip_code = models.CharField(_('zip code'), blank=True, max_length=6)
    state = models.CharField(_('state'), blank=True, max_length=50)
    country = models.CharField(_('country'), max_length=300)

    def __str__(self):
        return self.country + ', ' + self.state + ', ' + self.city
