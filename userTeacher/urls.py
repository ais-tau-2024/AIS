from django.urls import path
from .views import TeacherDetailByIINView, TeacherUpdateByIINView

urlpatterns = [
    path('teacher/<str:iin>/', TeacherDetailByIINView.as_view(), name='teacher-detail-by-iin'),
    path('teacher/<str:iin>/update/', TeacherUpdateByIINView.as_view(), name='teacher-update-by-iin'),
]