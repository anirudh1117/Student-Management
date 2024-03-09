from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from rest_framework import status

from utils.permissions import MyPermission
from .serializer import GroupSerializer, PermissionSerializer

class GroupList(APIView):
    permission_classes = [IsAuthenticated]
    #perm_slug = "trackActivity.ActivityLog"

    def get(self, request, format=None):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("context", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionList(APIView):
    permission_classes = [IsAuthenticated]
    #perm_slug = "trackActivity.ActivityLog"

    def get(self, request, format=None):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            context = {
                "message" : "Email is send with username and password to the registered user"
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)