from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from custom_auth.models import (TeacherModel,TeacherAchievementModel,
    TeacherScienceFieldModel,
    TeacherForeignLanguageModel,
    TeacherEducationRecordModel,
    TeacherCategoryModel)
from .serializers import (TeacherModelSerializer,TeacherAchievementSerializer,
    TeacherScienceFieldSerializer,
    TeacherForeignLanguageSerializer,
    TeacherEducationRecordSerializer,
    TeacherCategorySerializer)
from rest_framework.permissions import AllowAny

class TeacherDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, iin):
        """
        Получение информации о преподавателе по IIN.
        """

        try:
            teacher = TeacherModel.objects.get(iin=iin)
        except TeacherModel.DoesNotExist:
            return Response(
                {"error": "Преподаватель с таким IIN не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeacherModelSerializer(teacher)
        return Response(serializer.data)

class TeacherAchievementListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, teacher_id):
        achievements = TeacherAchievementModel.objects.filter(teacher_id=teacher_id)
        serializer = TeacherAchievementSerializer(achievements, many=True)
        return Response(serializer.data)

class TeacherScienceFieldListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, teacher_id):
        science_fields = TeacherScienceFieldModel.objects.filter(teacher_id=teacher_id)
        serializer = TeacherScienceFieldSerializer(science_fields, many=True)
        return Response(serializer.data)

class TeacherForeignLanguageListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, teacher_id):
        languages = TeacherForeignLanguageModel.objects.filter(teacher_id=teacher_id)
        serializer = TeacherForeignLanguageSerializer(languages, many=True)
        return Response(serializer.data)

class TeacherEducationRecordListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, teacher_id):
        education_records = TeacherEducationRecordModel.objects.filter(teacher_id=teacher_id)
        serializer = TeacherEducationRecordSerializer(education_records, many=True)
        return Response(serializer.data)

class TeacherCategoryListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, teacher_id):
        categories = TeacherCategoryModel.objects.filter(teacher_id=teacher_id)
        serializer = TeacherCategorySerializer(categories, many=True)
        return Response(serializer.data)