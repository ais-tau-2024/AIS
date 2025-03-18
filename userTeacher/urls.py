from django.urls import path
from .views import TeacherDetailByIINView, TeacherListView, TeacherUpdateByIINView

urlpatterns = [
    path('teacher/<str:iin>/', TeacherDetailByIINView.as_view(), name='teacher-detail-by-iin'),
    path('teacher/<str:iin>/update/', TeacherUpdateByIINView.as_view(), name='teacher-update-by-iin'),
    path('list/', TeacherListView.as_view())
]