from django.urls import path
from .views import DepartmentList, StaffList, DegreeList, DesignationList

urlpatterns = [
    path('department', DepartmentList.as_view(), name='departments'),
    path('', StaffList.as_view(), name='staff-list'),
    #path('<str:id>', StaffList.as_view(), name='add-user-staff'),
    path('degree', DegreeList.as_view(), name='degree'),
    path('designation', DesignationList.as_view(), name='designation'),
]
