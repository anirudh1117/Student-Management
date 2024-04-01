from rest_framework import status
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from schoolARP.customPagination import CustomPageNumberPagination
from utils.constants import STAFF
from utils.exceptions import InvalidUuidFormat
from trackActivity.mixins import ActivityLogMixin
from rest_framework.permissions import IsAuthenticated
from utils.permissions import MyPermission
from accounts.serializer import UserAccoutWriteSerializer

from .models import Department, Staff, Degree, Designation, StaffPreviousExperience, StaffEducation
from .serializer import DepartmentSerializer, StaffWriteSerializer, DegreeSerializer, DesignationSerializer
from .serializerRead import StaffSerializer


class DepartmentList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "staff.department"

    def get(self, request, format=None):
        departments = Department.objects.filter(school=request.user.school).order_by('updated_at')
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(departments, request)

        if page is not None:
            serializer = DepartmentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepartmentSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "staff.staff"

    def get(self, request, format=None):
        staffList = Staff.objects.filter(account__school=request.user.school).order_by("created_at")
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(staffList, request)

        if page is not None:
            serializer = StaffSerializer(
            page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)
            #return Response(serializer.data)
        
        serializer = StaffSerializer(
            staffList, many=True, context={"request": request})
        return Response(serializer.data)
    

    @transaction.atomic
    def post(self, request, format=None):
        request.data['role'] = STAFF
        request.data['school'] = request.user.school.id

        account_serializer = UserAccoutWriteSerializer(
            data=request.data, context={"request": request})
        if account_serializer.is_valid(raise_exception=True):
            account = account_serializer.save()
            request.data['account'] = account.id

            staff_serializer = StaffWriteSerializer(
                data=request.data, context={"request": request})
            if staff_serializer.is_valid(raise_exception=True):
                staff_serializer.save()

                context = {
                    "message": "Email is send with username and password to the registered Staff"
                }
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                return Response(staff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #def post(self, request, id, format=None):
    #    request.POST['account'] = id
    #    serializer = StaffWriteSerializer(
    #        data=request.data, context={"request": request})
    #    if serializer.is_valid(raise_exception=True):
    #        serializer.save()
    #        context = {
    #            "message": "Account is added in Staff"
    #        }
    #        return Response(context, status=status.HTTP_201_CREATED)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DegreeList(ActivityLogMixin, APIView):

    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "staff.degree"

    def get(self, request, format=None):
        degreeList = Degree.objects.all()
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(degreeList, request)

        if page is not None:
            serializer = DegreeSerializer(
            page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = DegreeSerializer(
            page, many=True, context={"request": request})
        return Response(serializer.data)


class DesignationList(ActivityLogMixin, APIView):

    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "staff.designation"

    def get(self, request, format=None):
        designationList = Designation.objects.filter(
            school=request.user.school)
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(designationList, request)

        if page is not None:
            serializer = DesignationSerializer(
            page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)
        serializer = DesignationSerializer(
            designationList, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DesignationSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
