from django.urls import path
from .views import StudentDetailView, StudentListView

urlpatterns = [
    path('list/', StudentListView.as_view()),
    path('<int:id>/', StudentDetailView.as_view(), name='student-detail'),
]
