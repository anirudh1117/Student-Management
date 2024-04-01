from django.urls import path
from .views import TeacherList

urlpatterns = [
    path('', TeacherList.as_view(), name='teacher'),
]
