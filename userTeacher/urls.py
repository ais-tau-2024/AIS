# userTeacher/urls.py

from django.urls import path

from .views import TeacherDetailView


urlpatterns = [
    path('teacher/<str:iin>/', TeacherDetailView.as_view(), name='teacher-detail'),
]
