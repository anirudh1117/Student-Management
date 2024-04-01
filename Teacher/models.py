from django.db import models
from django.db.models import Max
import datetime

from staff.models import Staff, Degree
from school.models import School

class Teacher(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    highest_degree = models.CharField(max_length=255, blank=True, null=True)
    years_of_experience = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.staff.account.first_name} - {self.years_of_experience}"

    def save(self, *args, **kwargs):
        self.update_highest_degree()
        self.update_years_of_experience()
        super().save(*args, **kwargs)

    def update_highest_degree(self):
        highest_degree_info = self.staff.education.aggregate(highest_prio=Max('degree__prio'))
        highest_prio = highest_degree_info.get('highest_prio')

        if highest_prio is not None:
            degree = Degree.objects.filter(prio=highest_prio).first()
            if degree:
                self.highest_degree = degree.name

    def update_years_of_experience(self):
        experiences = self.staff.experiences.all()
        total_years = 0
        for exp in experiences:
            if exp.end_date:
                total_years += (exp.end_date.year - exp.start_date.year)
            else:
                total_years += (datetime.datetime.now().year - exp.start_date.year)
        self.years_of_experience = total_years
