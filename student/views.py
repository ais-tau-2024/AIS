from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response  # ✅ Исправленный импорт
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from custom_auth.models import StudentModel
from custom_auth.serializers import StudentSerializer
from pyuca import Collator
from django.db.models import Q
from unidecode import unidecode

class StudentDetailView(APIView):  
    permission_classes = [AllowAny]

    def get(self, request, iin):
        student = StudentModel.objects.filter(iin=iin).first()  # Используем .first()

        if not student:
            return JsonResponse(data={"error": "Студент не найден"}, status=status.HTTP_404_NOT_FOUND)

        student_data = StudentSerializer(student)
        return JsonResponse(data=student_data.data, status=status.HTTP_200_OK)



class StudentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data
        })

# Поменять тут
class StudentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('query', '').strip()
        group_id = request.query_params.get('group')
        students = StudentModel.objects.all()

        if query:
            students = students.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(patronymic__icontains=query) |
                Q(iin__icontains=query)
            )

        if group_id:
            students = students.filter(group_id=group_id)

        collator = Collator()
        students = sorted(
            students,
            key=lambda s: collator.sort_key(f"{(s.first_name or '')} {(s.patronymic or '')}")
        )

        paginator = StudentPagination()
        paginated_qs = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(paginated_qs, many=True)

        return paginator.get_paginated_response(serializer.data)
