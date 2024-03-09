from django.urls import path
from .views import GroupList, PermissionList

urlpatterns = [
    path('',GroupList.as_view(),name='groups-list'),
    path('permission',PermissionList.as_view(),name='permissions-list'),
]