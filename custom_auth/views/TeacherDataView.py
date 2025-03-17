from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password

from custom_auth.decorator import auth_teacher
from ..models import TeacherModel
from ..serializers import TeacherSerializer  # Импортируем сериализатор
from rest_framework.permissions import AllowAny


class TeacherDataView(APIView):
    """
    Авторизация преподавателя
    """
    permission_classes = [AllowAny]

    @auth_teacher
    def get(self, request):
        """
        Получение данных о себе (Преподаватель)
        """
        teacher: TeacherModel = request.user

        if not teacher:
            return Response({"error": "Преподаватель не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher)  # Сериализуем объект
        return Response(serializer.data, status=status.HTTP_200_OK)
