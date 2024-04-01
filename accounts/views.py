from schoolARP.customPagination import CustomPageNumberPagination
from .models import UserAccount
from .serializer import UserAccountReadSerializer,UserAccoutWriteSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from trackActivity.mixins import ActivityLogMixin
from utils.permissions import MyPermission
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404


class UserAccountList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "accounts.useraccount"

    def get(self, request, format=None):
        userAccounts = UserAccount.objects.filter(school = request.user.school)
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(userAccounts, request)

        if page is not None:
            serializer = UserAccountReadSerializer(
            page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = UserAccountReadSerializer(userAccounts, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        serializer = UserAccoutWriteSerializer(data=request.data, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            context = {
                "message" : "Email is send with username and password to the registered user"
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountDetail(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "accounts.useraccount"
  
    def get_object(self, pk):
        try:
            return UserAccount.objects.get(id = pk)
        except:
            raise Http404

    def get(self, request, id, format=None):
        userAccount = self.get_object(id)
        serializer = UserAccountReadSerializer(userAccount, context={"request": request})
        return Response(serializer.data)

    def put(self, request, id, format=None):
        userAccount = self.get_object(id)
        serializer = UserAccoutWriteSerializer(userAccount, data=request.data, context={"request": request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        userAccount = self.get_object(id)
        userAccount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class CustomTokenObtainPairView(TokenObtainPairView, APIView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

