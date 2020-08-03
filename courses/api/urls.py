from django.urls import path,include
from .views import *
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('courses',CourseViewSet)
app_name = 'courses'
urlpatterns = [
    path('subjects/',SubjectListView.as_view(),name='subject_list'),
    path('subjects/<pk>/',SubjectDetailView.as_view(),name='subject_detail'),
    # path('courses/<pk>/enroll/',CourseEnrollView.as_view(),name='course_enroll'),
    path('',include(routers.urls)),
]