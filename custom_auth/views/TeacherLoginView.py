# custom_auth/views/TeacherLoginView.py
# Тут выполняется авторизация преподавателя по IIN и паролю. Cоздается модель Авторизации преподавателя и его токен.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
import secrets
from ..models import TeacherModel, TeacherAuthModel, TeacherAuthTokenModel
from rest_framework.permissions import AllowAny


class TeacherLoginView(APIView):
    """
    Авторизация преподавателя
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Авторизация преподавателя. Создаем токен по IIN и паролю.
        """
        iin = request.data.get('iin')
        password = request.data.get('password')

        # Проверка на наличие IIN и пароля
        if not iin or not password:
            return Response({"error": "IIN and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка на существование преподавателя
        teacher = TeacherModel.objects.filter(iin=iin).first()
        if not teacher:
            return Response({"error": "IIN or PASSWORD entered incorrectly"}, status=status.HTTP_404_NOT_FOUND)

        # Проверка на существование авторизационной записи
        teacher_auth = TeacherAuthModel.objects.filter(teacher=teacher).first()
        if not teacher_auth:
            return Response({"error": "Authorization data not found"}, status=status.HTTP_404_NOT_FOUND)

        # Проверка пароля
        if not check_password(password, teacher_auth.password):
            return Response({"error": "IIN or PASSWORD entered incorrectly"}, status=status.HTTP_401_UNAUTHORIZED)

        # Генерация рандомного токена
        ACTIVE_TOKEN = secrets.token_urlsafe(32)

        # Создание модели токена
        teacher_token = TeacherAuthTokenModel.objects.create(token=ACTIVE_TOKEN, teacher=teacher)

        # Возврат токена
        return Response({
            "message": "Token successfully created",
            "token": teacher_token.token
        }, status=status.HTTP_200_OK)






