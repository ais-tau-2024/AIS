# custom_auth/urls.py

from django.urls import path

# from custom_auth.views.AdminLoginView import AdminLoginView 
from custom_auth.views.TeacherLoginView import TeacherLoginView
from custom_auth.views.TeacherPasswordManagementView import TeacherPasswordManagementView

urlpatterns = [
    # path('admin/login', AdminLoginView.as_view()),
    path('teacher/login', TeacherLoginView.as_view()),
    path('teacher/password', TeacherPasswordManagementView.as_view()),
]





