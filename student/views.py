from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response  # ✅ Исправленный импорт
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
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


class StudentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = StudentModel.objects.all()
        paginator = StudentPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = StudentSerializer(paginated_qs, many=True)

        return paginator.get_paginated_response(serializer.data)