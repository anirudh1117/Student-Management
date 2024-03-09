from django.db import models


class School(models.Model):
    registerationnumber = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100)
    phoneNo = models.CharField(blank=True, max_length=10, null=True)
    logo = models.ImageField(
        upload_to='photos/school/%Y/%m/%d/', blank=True, null=True)
    line1 = models.CharField(blank=True, max_length=150)
    city = models.CharField(max_length=300)
    zip_code = models.CharField(blank=True, max_length=6)
    state = models.CharField(blank=True, max_length=50)
    country = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    current_session = models.OneToOneField(
        'Session', on_delete=models.SET_NULL, null=True, blank=True, related_name='currentSession')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.city} - {self.email}"


class Session(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='schoolSessions')
    name = models.CharField(max_length=100, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.school.name} ({self.start_date} - {self.end_date})"
