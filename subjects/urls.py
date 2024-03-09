from django.urls import path
from .views import CoursesList

urlpatterns = [
    path('',CoursesList.as_view(),name='courses'),
]