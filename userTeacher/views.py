from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from custom_auth.decorator import auth_teacher
from custom_auth.models import TeacherModel
from .serializers import TeacherSerializer
from custom_auth.serializers import TeacherAchievementSerializer, TeacherCategorySerializer, TeacherEducationRecordSerializer, TeacherForeignLanguageSerializer, TeacherGroupSerializer, TeacherScienceFieldSerializer, TeacherSerializer as AuthTeacherSerializer
import logging
from pyuca import Collator
from django.db.models import Q
from unidecode import unidecode

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
        

class TeacherPagination(PageNumberPagination):
    page_size = 10  # или взять из query params
    page_size_query_param = 'page_size'
    max_page_size = 100


# Поменять тут
class TeacherListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('query', '').strip()
        teachers = TeacherModel.objects.all()
        
        if query:
            query = query.lower()
            teachers = [t for t in teachers if
                        query in (t.first_name or '').lower() or
                        query in (t.last_name or '').lower() or
                        query in (t.patronymic or '').lower() or
                        query in (t.iin or '').lower()]

        collator = Collator()
        teachers = sorted(teachers, key=lambda t: collator.sort_key(f"{t.last_name or ''} {(t.first_name or '')} {(t.patronymic or '')}"))

        paginator = TeacherPagination()
        paginated_qs = paginator.paginate_queryset(teachers, request)
        serializer = AuthTeacherSerializer(paginated_qs, many=True)

        return paginator.get_paginated_response(serializer.data)


class TeacherDataView(APIView):
    """
    Авторизация преподавателя
    """
    permission_classes = [AllowAny]

    @auth_teacher
    def get(self, request):
        teacher: TeacherModel = request.user

        if not teacher:
            return Response({"error": "Преподаватель не найден"}, status=status.HTTP_404_NOT_FOUND)

        data = AuthTeacherSerializer(teacher).data

        if request.headers.get('Additional-Info'):
            data['achievements'] = TeacherAchievementSerializer(teacher.achievements.all(), many=True).data
            data['science_fields'] = TeacherScienceFieldSerializer(teacher.science_fields.all(), many=True).data
            data['foreign_languages'] = TeacherForeignLanguageSerializer(teacher.foreign_languages.all(), many=True).data
            data['education_records'] = TeacherEducationRecordSerializer(teacher.education_records.all(), many=True).data
            data['categories'] = TeacherCategorySerializer(teacher.categories.all(), many=True).data
            data['groups'] = TeacherGroupSerializer(teacher.teacher_groups.all(), many=True).data

        return Response(data, status=status.HTTP_200_OK)
