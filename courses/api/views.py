from rest_framework.generics import ListAPIView,RetrieveAPIView

from courses.api.permissions import IsEnrolled
from ..models import Subject,Course
from .serializers import SubjectSerializer,CourseSerializer,CourseWithContentsSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action


class SubjectListView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CourseEnrollView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    def post(self,request,pk,format=None):
        course = get_object_or_404(Course,pk=pk)
        course.students.add(request.user)
        return Response({'enrolled':True})

class CourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(methods=['post'],detail=True,authentication_classes=[BasicAuthentication],permission_classes=[IsAuthenticated])
    def enroll(self,request,*args,**kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled':True})


    @action(methods=['get'],detail=True,serializer_class=CourseWithContentsSerializer,authentication_classes=[BasicAuthentication],permission_classes=[IsAuthenticated,IsEnrolled])
    def contents(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)