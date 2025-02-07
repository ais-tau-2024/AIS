# custom_auth/views/TeacherPasswordManagementView.py
# Тут выполняется управление паролем преподавателя. Метод get проверяет наличие пароля у преподавателя. Метод post изменяет пароль по ИИН.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from ..models import TeacherModel, TeacherAuthModel
from rest_framework.permissions import AllowAny


class TeacherPasswordManagementView(APIView):
    """
    Управление паролем преподавателя
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Проверка. Установлен ли пароль. Если пароль установлен то возвращается статус 200.
        """
        iin = request.GET.get('iin', '')

        # Проверка на наличие IIN
        if not iin:
            return Response({"error": "IIN is required"}, status=status.HTTP_400_BAD_REQUEST)


        # Проверка существования преподавателя
        try:
            teacher = TeacherModel.objects.filter(iin=iin).first()
        except Exception as e:
            print(e)
        if not teacher:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        # Проверка на существование записи авторизации
        teacher_auth = TeacherAuthModel.objects.filter(teacher=teacher).exists()
        if teacher_auth:
            return Response({"status": "Password already set"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Password not set"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def post(self, request):
        """
        Смена пароля по ИИН
        """
        iin = request.data.get('iin')
        new_password = request.data.get('password')

        # Проверка на наличие данных
        if not iin or not new_password:
            return Response({"error": "IIN and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка существования преподавателя
        teacher = TeacherModel.objects.filter(iin=iin).first()
        if not teacher:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        # Получение или создание записи авторизации
        teacher_auth, created = TeacherAuthModel.objects.get_or_create(teacher=teacher)

        # Установка нового пароля
        teacher_auth.password = make_password(new_password)
        teacher_auth.save()

        return Response({"message": "Password successfully updated"}, status=status.HTTP_200_OK)
