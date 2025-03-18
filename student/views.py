from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response  # ✅ Исправленный импорт
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from custom_auth.models import StudentModel
from custom_auth.serializers import StudentSerializer

class StudentDetailView(APIView):  # Можно тоже заменить на APIView для консистентности
    def get(self, request, id):
        student = get_object_or_404(StudentModel, id=id)
        data = {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "patronymic": student.patronymic,
            "group": student.group.name if student.group else None,
            "birth_date": student.birth_date,
            "gender": student.gender,
            "nationality": student.nationality,
            "marital_status": student.marital_status,
            "citizenship": student.citizenship,
            "country_of_origin": student.country_of_origin,
            "place_of_birth": student.place_of_birth,
            "was_born_in_another_country": student.was_born_in_another_country,
        }
        return JsonResponse(data)

class StudentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        students = StudentSerializer(StudentModel.objects.all(), many=True)
        return Response(students.data, status=status.HTTP_200_OK)
