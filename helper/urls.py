# helpers/urls.py

from django.urls import path
from .views import ProxyAutocompleteView, list_routes

urlpatterns = [
    path("autocomplete/", ProxyAutocompleteView.as_view()),
    path("routes/", list_routes),
]

