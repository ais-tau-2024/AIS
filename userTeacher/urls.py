from django.urls import path

from .views import TeacherDetailByIINView, TeacherListView, TeacherUpdateByIINView, TeacherDataView

urlpatterns = [
    path('me/', TeacherDataView.as_view()),
    path('list/', TeacherListView.as_view()),
    path('<str:iin>/', TeacherDetailByIINView.as_view()),
    path('<str:iin>/update/', TeacherUpdateByIINView.as_view()),
]