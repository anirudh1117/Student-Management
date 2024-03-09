from django.urls import path
from .views import StudentList, GuardianList

urlpatterns = [
    path('',StudentList.as_view(),name='student'),
    path('guardian',GuardianList.as_view(),name='guardian'),
]