from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response  # ✅ Исправленный импорт
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from custom_auth.models import StudentModel
from custom_auth.serializers import StudentSerializer

class StudentDetailView(APIView):  
    permission_classes = [AllowAny]

    def get(self, request, iin):
        student = StudentModel.objects.filter(iin=iin).first()  # Используем .first()

        if not student:
            return JsonResponse(data={"error": "Студент не найден"}, status=status.HTTP_404_NOT_FOUND)

        student_data = StudentSerializer(student)
        return JsonResponse(data=student_data.data, status=status.HTTP_200_OK)


class StudentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        students = StudentSerializer(StudentModel.objects.all(), many=True)
        return Response(students.data, status=status.HTTP_200_OK)
