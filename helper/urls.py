# helpers/urls.py

from django.urls import path
from .views import ProxyAutocompleteView

urlpatterns = [
    path("autocomplete/", ProxyAutocompleteView.as_view(), name="autocomplete"),
]

