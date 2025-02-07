# fileManager/urls.py

from django.urls import path

from .views import DirManagerView, FileManagerView


urlpatterns = [
    path('dir', DirManagerView.as_view()),
    path('file', FileManagerView.as_view()),
]





