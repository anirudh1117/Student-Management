from django.urls import path
from .views import ExamsList, MarksList, CourseScheduleList

urlpatterns = [
    path('',ExamsList.as_view(),name='exams'),
    path('marks',MarksList.as_view(),name='marks'),
    path('<str:id>/schedule-course',CourseScheduleList.as_view(), name="course-schedule")
]