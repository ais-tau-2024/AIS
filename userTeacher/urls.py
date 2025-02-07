# userTeacher/urls.py

from django.urls import path

from userTeacher.views.TeacherView import TeacherView
from userTeacher.views.GroupView import GroupView


urlpatterns = [
    path("", TeacherView.as_view()),
    path("group", GroupView.as_view())
]
