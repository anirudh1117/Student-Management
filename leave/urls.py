from django.urls import path
from .views import LeaveTypeList, LeaveList

urlpatterns = [
    path('',LeaveList.as_view(),name='leaves-list'),
    path('type',LeaveTypeList.as_view(),name='leaves-type'),
]