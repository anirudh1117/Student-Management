from django.urls import path
from .views import ActivityLogList

urlpatterns = [
    path('',ActivityLogList.as_view(),name='Activity-log'),
]