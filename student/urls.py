from django.urls import path
from .views import StudentDetailView, StudentListView

urlpatterns = [
    path('list/', StudentListView.as_view()),
    path('<str:iin>/', StudentDetailView.as_view()),
]
