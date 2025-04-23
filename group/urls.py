from django.urls import path
from .views import GroupListView

urlpatterns = [
    path('list/', GroupListView.as_view(), name='group-list'),
]
