# django_admin/urls.py

import os
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import include, path
from django.conf import settings
from filebrowser.sites import site

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def serve_media(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return HttpResponse(f.read(), content_type="application/octet-stream")
    return HttpResponse("File not found", status=404)

def render_template_v1(request):
    return render(request, 'index_v1.html')


def render_template_v2(request):
    return render(request, 'index_v2.html')

urlpatterns = [
    path('v1/', render_template_v1),
    path('v2/', render_template_v2),
    # Пути настройки
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # Пути API
    path('auth/', include('custom_auth.urls')), 
    path('fileManager/', include('fileManager.urls')),
    path('userTeacher/', include('userTeacher.urls')),
    path('helper/', include('helper.urls')),
    path('userStudent/', include('student.urls')),

    path('media/<path:filename>', serve_media, name='media_file'),
]