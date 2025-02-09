from django.urls import path
from .views import TeacherDetailByIINView

urlpatterns = [
    path('teacher/<str:iin>/', TeacherDetailByIINView.as_view(), name='teacher-detail-by-iin'),
]
