from django.urls import path
from .views import ClassList, ClassDetail, SectionList, SectionDetail

urlpatterns = [
    path('',ClassList.as_view(),name='class-list'),
    path('<str:id>',ClassDetail.as_view(),name='class-detail'),
    path('<str:id>/section',SectionList.as_view(),name='section-list'),
    path('section/<str:id>',SectionDetail.as_view(),name='section-detail'),
]