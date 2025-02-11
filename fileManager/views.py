import os
import shutil
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from custom_auth.decorator import auth_teacher
from .models import Desktop, DesktopAccess
from .authentication import TeacherTokenAuthentication
from custom_auth.models import TeacherModel
from rest_framework.permissions import AllowAny

class CreateDesktopView(APIView):
    permission_classes = [AllowAny]

    @auth_teacher
    def post(self, request):
        name = request.data.get('name', 'Новый рабочий стол')
        desktop = Desktop.objects.create(teacher=request.user, name=name)
        os.makedirs(desktop.get_path(), exist_ok=True)
        return Response({'id': desktop.id, 'name': desktop.name}, status=status.HTTP_201_CREATED)


class ListDesktopsView(APIView):
    permission_classes = [AllowAny]

    @auth_teacher
    def get(self, request):
        owned = Desktop.objects.filter(teacher=request.user)
        shared = Desktop.objects.filter(access_list__teacher=request.user)
        desktops = (owned | shared).distinct()
        data = [{'id': d.id, 'name': d.name, 'owner': d.teacher.id} for d in desktops]
        return Response(data)


class DeleteDesktopView(APIView):
    permission_classes = [AllowAny]

    @auth_teacher
    def delete(self, request, desktop_id):
        try:
            desktop = Desktop.objects.get(id=desktop_id)
        except Desktop.DoesNotExist:
            return Response({'error': 'Рабочий стол не найден'}, status=status.HTTP_404_NOT_FOUND)
        if desktop.teacher != request.user:
            return Response({'error': 'Удалять может только создатель'}, status=status.HTTP_403_FORBIDDEN)
        shutil.rmtree(desktop.get_path(), ignore_errors=True)
        desktop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GrantAccessView(APIView):
    permission_classes = [AllowAny]

    @auth_teacher
    def post(self, request, desktop_id):
        teacher_id = request.data.get('teacher_id')
        if not teacher_id:
            return Response({'error': 'teacher_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            desktop = Desktop.objects.get(id=desktop_id)
        except Desktop.DoesNotExist:
            return Response({'error': 'Рабочий стол не найден'}, status=status.HTTP_404_NOT_FOUND)
        if desktop.teacher != request.user:
            return Response({'error': 'Доступ может дать только владелец'}, status=status.HTTP_403_FORBIDDEN)
        try:
            target_teacher = TeacherModel.objects.get(id=teacher_id)
        except TeacherModel.DoesNotExist:
            return Response({'error': 'Преподаватель не найден'}, status=status.HTTP_404_NOT_FOUND)
        DesktopAccess.objects.get_or_create(desktop=desktop, teacher=target_teacher)
        return Response({'message': 'Доступ предоставлен'})


class ListFilesView(APIView):
    permission_classes = [AllowAny]

    @auth_teacher
    def get(self, request, desktop_id):
        relative_path = request.query_params.get('path', '')
        try:
            desktop = Desktop.objects.get(id=desktop_id)
        except Desktop.DoesNotExist:
            return Response({'error': 'Рабочий стол не найден'}, status=status.HTTP_404_NOT_FOUND)
        # Проверка доступа: владелец или доступ через DesktopAccess
        if desktop.teacher != request.user and not DesktopAccess.objects.filter(desktop=desktop, teacher=request.user).exists():
            return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)
        base_path = desktop.get_path()
        target_path = os.path.join(base_path, relative_path.lstrip('/'))
        if not os.path.exists(target_path):
            return Response({'error': 'Путь не существует'}, status=status.HTTP_400_BAD_REQUEST)
        result = {'directories': [], 'files': []}
        for item in os.listdir(target_path):
            full_item = os.path.join(target_path, item)
            if os.path.isdir(full_item):
                result['directories'].append(item)
            elif os.path.isfile(full_item):
                ext = os.path.splitext(item)[1]
                result['files'].append({'name': item, 'type': ext})
        return Response(result)


class UploadFileView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]

    @auth_teacher
    def post(self, request, desktop_id):
        relative_path = request.data.get('path', '')
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'Файл не передан'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            desktop = Desktop.objects.get(id=desktop_id)
        except Desktop.DoesNotExist:
            return Response({'error': 'Рабочий стол не найден'}, status=status.HTTP_404_NOT_FOUND)
        if desktop.teacher != request.user and not DesktopAccess.objects.filter(desktop=desktop, teacher=request.user).exists():
            return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)
        target_dir = os.path.join(desktop.get_path(), relative_path.lstrip('/'))
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, file_obj.name), 'wb+') as dest:
            for chunk in file_obj.chunks():
                dest.write(chunk)
        return Response({'message': 'Файл загружен'}, status=status.HTTP_201_CREATED)


class FileActionView(APIView):
    permission_classes = [AllowAny]

    @auth_teacher
    def delete(self, request, desktop_id):
        relative_path = request.data.get('path', '')
        try:
            desktop = Desktop.objects.get(id=desktop_id)
        except Desktop.DoesNotExist:
            return Response({'error': 'Рабочий стол не найден'}, status=status.HTTP_404_NOT_FOUND)
        if desktop.teacher != request.user and not DesktopAccess.objects.filter(desktop=desktop, teacher=request.user).exists():
            return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)
        target = os.path.join(desktop.get_path(), relative_path.lstrip('/'))
        if os.path.isfile(target):
            os.remove(target)
            return Response({'message': 'Файл удалён'})
        return Response({'error': 'Файл не найден'}, status=status.HTTP_400_BAD_REQUEST)

    @auth_teacher
    def put(self, request, desktop_id):
        old_path = request.data.get('old_path', '')
        new_name = request.data.get('new_name', '')
        if not new_name:
            return Response({'error': 'Новое имя обязательно'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            desktop = Desktop.objects.get(id=desktop_id)
        except Desktop.DoesNotExist:
            return Response({'error': 'Рабочий стол не найден'}, status=status.HTTP_404_NOT_FOUND)
        if desktop.teacher != request.user and not DesktopAccess.objects.filter(desktop=desktop, teacher=request.user).exists():
            return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)
        base_path = desktop.get_path()
        old_file = os.path.join(base_path, old_path.lstrip('/'))
        new_file = os.path.join(os.path.dirname(old_file), new_name)
        if os.path.isfile(old_file):
            os.rename(old_file, new_file)
            return Response({'message': 'Файл переименован'})
        return Response({'error': 'Файл не найден'}, status=status.HTTP_400_BAD_REQUEST)
