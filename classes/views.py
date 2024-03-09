from classes.models import Class, Section
from classes.serializer import ClassSerializer, SectionSerializer, ClassReadSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404
from utils.commonFunction import is_valid_uuid,string_to_uuid
from utils.exceptions import InvalidUuidFormat
from utils.permissions import MyPermission
from trackActivity.mixins import ActivityLogMixin


class ClassList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "classes.class"

    def get(self, request, format=None):
        classes = Class.objects.filter(school = request.user.school)
        className = request.GET.get('className', '')
        if className != '':
            classes = classes.filter(name__iexact=className)
        serializer = ClassReadSerializer(classes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClassSerializer(data=request.data, context = {'request' : request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassDetail(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "classes.class"
  
    def get_object(self, pk):
        try:
            if is_valid_uuid(pk):
                uuid = string_to_uuid(pk)
                return Class.objects.get(id = uuid)
            else:
                raise InvalidUuidFormat()
        except:
            raise Http404

    def get(self, request, id, format=None):
        class_object = self.get_object(id)
        serializer = ClassReadSerializer(class_object)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        class_object = self.get_object(id)
        serializer = ClassSerializer(class_object, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        class_object = self.get_object(id)
        class_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SectionList(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "classes.section"

    def get(self, request, id, format=None):
        sections = Section.objects.filter(classID=id).filter(school = request.user.school)
        sectionName = request.GET.get('sectionName', '')
        if sectionName != '':
            sections = sections.filter(name__iexact=sectionName)
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        serializer = SectionSerializer(data=request.data, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionDetail(ActivityLogMixin, APIView):
    permission_classes = [IsAuthenticated, MyPermission]
    perm_slug = "classes.section"
  
    def get_object(self, pk):
        try:
            if is_valid_uuid(pk):
                uuid = string_to_uuid(pk)
                return Section.objects.get(id = uuid)
            else:
                raise InvalidUuidFormat()
        except:
            raise Http404

    def get(self, request, id, format=None):
        section_object = self.get_object(id)
        serializer = SectionSerializer(section_object)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        section_object = self.get_object(id)
        serializer = SectionSerializer(section_object, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        section_object = self.get_object(id)
        section_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
