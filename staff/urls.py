from django.urls import path
from .views import DepartmentList, StaffList

urlpatterns = [
    path('department',DepartmentList.as_view(),name='departments'),
    path('',StaffList.as_view(),name='staff-list'),
    path('<str:id>',StaffList.as_view(),name='add-user-staff'),
]