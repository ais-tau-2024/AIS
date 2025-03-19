from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound
from custom_auth.decorator import auth_teacher
from custom_auth.models import TeacherModel
from .serializers import TeacherSerializer
from custom_auth.serializers import TeacherSerializer as AuthTeacherSerializer
import logging

# Logger не обязателен
logger = logging.getLogger(__name__)

class TeacherDetailByIINView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = TeacherModel.objects.all()
    serializer_class = AuthTeacherSerializer
    lookup_field = 'iin'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        try:
            return queryset.get(**filter_kwargs)
        except TeacherModel.DoesNotExist:
            raise NotFound({"error": "Teacher with the provided IIN not found."})

class TeacherUpdateByIINView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, iin):
        try:
            teacher = TeacherModel.objects.get(iin=iin)
        except TeacherModel.DoesNotExist:
            return Response({"error": "Teacher with the provided IIN not found."},
                          status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating teacher with IIN {iin}: {str(e)}")
            return Response({"error": "Internal server error"},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TeacherListView(APIView):
    permission_classes = [AllowAny]

    @auth_teacher
    def get(self, request):
        teachers = AuthTeacherSerializer(TeacherModel.objects.all(), many=True)
        return Response(teachers.data, status=status.HTTP_200_OK)

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

        serializer = AuthTeacherSerializer(teacher)  # Сериализуем объект
        return Response(serializer.data, status=status.HTTP_200_OK)
