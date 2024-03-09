from django.urls import path
from .views import HoldiaysList, StudentAttendanceList

urlpatterns = [
    path('holiday',HoldiaysList.as_view(),name='holidays-list'),
    path('student',StudentAttendanceList.as_view(),name='student-attendance-list'),
]