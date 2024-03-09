from django.urls import path
from .views import UserAccountList, UserAccountDetail, CustomTokenObtainPairView, CustomTokenRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('',UserAccountList.as_view(),name='account'),
    path('<str:id>',UserAccountDetail.as_view(),name='accountsDetail'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]